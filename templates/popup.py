def friends():
    """Allow user to follow their friends and see their current location in a table"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username=request.form.get("username") # search for friend's username

        # Ensure username is entered
        if not username:
            return apology("must provide username", 403)
        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
            return apology("TODO")
        # Ensure username exists before following friend
        if len(rows) != 1:
            return apology("invalid username" , 403)
        else:
            return apology("TODO")
            #TODO update queries to establish follower/followee relationship

        return redirect("/friends")

    else:
        # query to get your friends and their current locations
        return render_template("friends.html", userinfo=session.get("userinfo"))
