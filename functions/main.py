import functions_framework
import firebase_admin
from firebase_admin import firestore
import datetime

#initialize app
app = firebase_admin.initialize_app()


@functions_framework.http
def viewcount_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}
    
    #initialize db
    db = firestore.client()
    
    #update + acquire current visit number
    visits_ref = db.collection("visits")
    visits = visits_ref.document('0').get(field_paths={'views'}).to_dict().get('views')
    visits += 1
    visits_ref.document("0").set({'views':visits})

    #acquire data for fields
    ip = request.remote_addr
    timeAccessed = datetime.datetime.now()

    #initialize new document with data
    doc_ref = visits_ref.document(str(visits))
    doc_ref.set({'visitID': visits, 'ip' : ip, 'timeAccessed' : timeAccessed})

    #return current visit number for counter
    return ("{}".format(visits), 200, headers)