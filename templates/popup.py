@app.route("/check", methods=["GET", "POST"])
def popup(loc):
    """Allow user to follow their friends and see their current location in a table"""
    if request.method == "POST":
            rows = db.execute("SELECT numpeople FROM locations WHERE location = :loc", locations=loc)
        return redirect("/maps")

  
