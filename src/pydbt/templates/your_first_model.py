def run(con, ibis):
    """
    Example model that creates a simple transformation.
    
    Args:
        con: Ibis connection
        ibis: Ibis module
        
    Returns:
        ibis.Expr: An Ibis expression that will be compiled to SQL
    """
    # Example: Calculate daily user registrations
    users = con.table('users')
    return users.group_by('registration_date').aggregate(
        daily_registrations=lambda t: t.id.count()
    ).order_by('registration_date')