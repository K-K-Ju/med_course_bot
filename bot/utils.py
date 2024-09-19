from bot.models import Res, Ok, Error


def run_query(query) -> Res:
    res = query()
    if res:
        return Ok(res)
    else:
        return Error('No records were found')
