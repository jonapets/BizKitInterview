from flask import Blueprint, request

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    search_params = request.args.to_dict()
    results = search_users(search_params)
    return {"results": results}, 200

def search_users(search_params):
    """Search users database

    Parameters:
        search_params: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match any of the provided search parameters
    """
    results_set = set()

    if "id" in search_params:
        user_id = search_params["id"]
        results_set = {user_id}

    if "name" in search_params:
        name_query = search_params["name"].lower()
        results_set.update(user["id"] for user in USERS if name_query in user["name"].lower())

    if "age" in search_params:
        age = int(search_params["age"])
        results_set.update(user["id"] for user in USERS if age - 1 <= user["age"] <= age + 1)

    if "occupation" in search_params:
        occupation_query = search_params["occupation"].lower()
        results_set.update(user["id"] for user in USERS if occupation_query in user["occupation"].lower())

    if not search_params:  # Return all users if no search parameters are provided
        results_set.update(user["id"] for user in USERS)

    results = [user for user in USERS if user["id"] in results_set]

    # Sorting the results based on the specified priority
    results = sorted(results, key=lambda x: (
        x.get("id", ""),
        x.get("name", "").lower(),
        x.get("age", 0),
        x.get("occupation", "").lower()
    ))

    # Sorting the results based on the order in which they were matched
    results = sorted(results, key=lambda x: list(search_params.keys()).index(next(key for key in search_params.keys() if key in x)), reverse=True)

    return results