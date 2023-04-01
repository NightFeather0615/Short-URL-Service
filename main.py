from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi import FastAPI, Path, Query
from deta import Deta

deta = Deta()
db = deta.Base("target_code")
app = FastAPI()

@app.get("/{code}")
def read_item(code: Annotated[str, Path(title="Short URL Code")], response: Response):
  print(db.get(code))
  if (shortcut_data := db.get(code)) is not None:
    response.status_code = status.HTTP_308_PERMANENT_REDIRECT
    return RedirectResponse(
      shortcut_data["target"],
      status_code = 308
    )
  else:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {
      "msg": "Short URL not found."
    }
