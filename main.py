from datetime import datetime
from os import environ, path
from traceback import format_exc

from pydantic import ValidationError

from src.api import (
    APIClient,
    CaptchaException,
    LoginException,
    NotFoundException,
    UnauthorizedException,
)
from src.database import Database
from src.schema import DatabaseEntry, Summary, User
from src.synchronizer import check_database_change, sync_database_with_summaries


def log(message: str) -> None:
    print(f"[JDV] {message}")


def run() -> tuple[bool, bool]:
    # Initialize environment.
    base_api_url = "https://www.duolingo.com"
    username = environ["DUOLINGO_USERNAME"]
    credential, passwordless = (
        (credential, True)
        if (credential := environ.get("DUOLINGO_JWT")) is not None
        else (environ["DUOLINGO_PASSWORD"], False)
    )

    # Declare paths.
    progression_database_path = path.join("data", "duolingo-progress.json")
    statistics_database_path = path.join("data", "statistics.json")

    # Initialize required infrastructures.
    api = APIClient(base_url=base_api_url)
    progression_database = Database(filename=progression_database_path)
    statistics_database = Database(filename=statistics_database_path)

    # If the supplied credential is the password, login to Duolingo first.
    token, passwordless = (
        (credential, True) if passwordless else (api.login(username, credential), False)
    )

    # Get the possible data.
    raw_user, raw_summary = api.fetch_data(username, token)
    
    # Debug: Log the raw API response
    log(f"Raw user data: {raw_user}")
    log(f"Raw summary data: {raw_summary}")
    
    if raw_summary.get("summaries") and len(raw_summary["summaries"]) > 0:
        log(f"First summary entry: {raw_summary['summaries'][0]}")
    else:
        log("No summaries found in API response")

    # Transform them into our internal schema.
    user = User(**raw_user)
    summaries = [Summary(**summary) for summary in raw_summary["summaries"]]

    # Get all existing data from the database. Add the new data to the end of the database
    # declaratively. `0` means the first entry, or today (when the script is run). Initially,
    # we try to transform the existing data from the database into our own structure so it's easier
    # to process.
    current_progression = progression_database.get()
    
    # Handle case where database starts as empty list
    if isinstance(current_progression, list):
        current_progression = {}
    
    database_entries: dict[str, DatabaseEntry] = {
        **{key: DatabaseEntry(**entry) for key, entry in current_progression.items()},
        **{summaries[0].date: DatabaseEntry.create(summaries[0], user.site_streak)},
    }

    # Synchronize the database with the summaries.
    synchronized_database = sync_database_with_summaries(database_entries, summaries)

    # Check whether we have synchronized the data or not.
    is_database_changed = check_database_change(synchronized_database, database_entries)

    # Store the synchronized database in our repository.
    progression_database.set(
        {key: value.model_dump() for key, value in synchronized_database.items()}
    )

    # On the other hand, get all of the statistics of the cron run, and then immutably
    # add the current cron statistics.
    current_date = datetime.now().strftime("%Y/%m/%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    current_statistics = statistics_database.get()
    statistics_entries: dict[str, str] = {
        **current_statistics,
        **{current_date: current_time},
    }

    # Store the statistics in our repository.
    statistics_database.set(statistics_entries)

    # Return flags from the program to consolidate the print statements in the outer loop,
    # minimizing side effects.
    return passwordless, is_database_changed


def main() -> None:
    log("Script is starting and running now.")
    try:
        passwordless, is_database_changed = run()
        match passwordless:
            case True:
                log("Script authenticated with your JWT.")
            case False:
                log("Script authenticated with your password. Please change it to JWT.")

        match is_database_changed:
            case True:
                log(
                    "Script found discrepancies between current data and online data. Synchronization is done automatically."
                )
            case False:
                log(
                    "Script did not find discrepancies between current data and online data. Synchronization not required."
                )

        log(
            "Script run successfully! Please check the specified path to see your newly updated data."
        )
    except ValidationError as error:
        log(
            f"Error encountered when parsing data. Potentially, a breaking API change: {error}"
        )
        log("This usually means the API response format has changed or contains unexpected null values.")
        log("Check the debug output above to see the actual API response.")
    except (
        CaptchaException,
        LoginException,
        NotFoundException,
        UnauthorizedException,
    ) as error:
        log(f"{error.__class__.__name__}: {error}")
    except Exception as error:
        log(f"Unexpected Exception: {error.__class__.__name__}: {error}")
        log(format_exc())
    finally:
        log("Japanese Duolingo Visualizer script has finished running.")


if __name__ == "__main__":
    main()
