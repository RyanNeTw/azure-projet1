import azure.functions as func
import datetime
import json
import uuid
import logging

app = func.FunctionApp()

@app.function_name(name="postUser")
@app.route(route="postUser", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="bayroumeterdb",
    container_name="users",
    create_if_not_exists=True
)
def post_user(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info("Processing POST /postUser")

    try:
        body = req.get_json()
        pseudo = body.get("pseudo")
        email = body.get("email")

        if not pseudo or email is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: pseudo, email"}),
                mimetype="application/json",
                status_code=400
            )

        document = {
            "id": str(uuid.uuid1()),
            "pseudo": pseudo,
            "email": email,
            "createdAt": datetime.datetime.utcnow().isoformat()
        }

        outputDocument.set(func.Document.from_dict(document))

        return func.HttpResponse(
            json.dumps({"status": "User created", "document": document}),
            mimetype="application/json",
            status_code=201
        )

    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )



@app.function_name(name="getUser")
@app.route(route="getUser", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="inputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="bayroumeterdb",
    container_name="users",
    sql_query="SELECT * FROM c WHERE c.pseudo = {pseudo} And c.email = {email}"
)
def get_user(req: func.HttpRequest, inputDocument: func.DocumentList) -> func.HttpResponse:
    logging.info("Processing GET /getUser")

    pseudo = req.params.get("pseudo")
    email = req.params.get('email')
    if not pseudo or not email:
        return func.HttpResponse(
            json.dumps({"error": "Missing query parameter: email or pseudo"}),
            mimetype="application/json",
            status_code=400
        )

    if inputDocument and len(inputDocument) > 0:
        document = inputDocument[0]
        return func.HttpResponse(
            body=json.dumps(document.to_dict()),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({"error": f"No data found for {pseudo, email}"}),
            mimetype="application/json",
            status_code=404
        )


@app.function_name(name="postVote")
@app.route(route="postVote", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="userDocs",
    connection="COSMOS_CONN_STRING",
    database_name="bayroumeterdb",
    container_name="users",
    sql_query="SELECT * FROM c WHERE c.pseudo = {pseudo} AND c.email = {email}"
)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="bayroumeterdb",
    container_name="votes",
    create_if_not_exists=True
)
def post_vote(req: func.HttpRequest, userDocs: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info("Processing POST /postVote")
    try:
        body = req.get_json()
        email = body.get("email")
        pseudo = body.get("pseudo")
        vote = body.get("vote")

        if not email or not pseudo:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: pseudo, email"}),
                mimetype="application/json",
                status_code=400
            )

        if not userDocs or len(userDocs) == 0:
            return func.HttpResponse(
                json.dumps({"error": "User not found"}),
                mimetype="application/json",
                status_code=404
            )

        user = userDocs[0]
        user_id = user["id"]

        document = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "vote": True if str(vote).lower() == "true" else False,
            "createdAt": datetime.datetime.utcnow().isoformat()
        }

        outputDocument.set(func.Document.from_dict(document))

        return func.HttpResponse(
            json.dumps({"status": "Vote created", "document": document}),
            mimetype="application/json",
            status_code=201
        )

    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

@app.function_name(name="getVotes")
@app.route(route="getVotes", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="inputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="bayroumeterdb",
    container_name="votes",
    sql_query="SELECT * FROM c"
)
def get_vote(req: func.HttpRequest, inputDocument: func.DocumentList) -> func.HttpResponse:
    logging.info("Processing GET /getVotes")

    if inputDocument and len(inputDocument) > 0:
        return func.HttpResponse(
            body=json.dumps(inputDocument, default=vars),
            mimetype="application/json",
            status_code=200
        )
    else:
        return func.HttpResponse(
            json.dumps({"error": f"No data found"}),
            mimetype="application/json",
            status_code=404
        )