def popup(location):
    """Allow user to follow their friends and see their current location in a table"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "CLICK":
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        return redirect("/maps")

  
