import pandas as pd

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
    try:
        users = con.table('users')
    except Exception:
        users = con.create_table('users', pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'registration_date': [
                '2024-01-01',
                '2024-01-01',
                '2024-01-02',
                '2024-01-02',
                '2024-01-03'
            ]
        }))
    return users.group_by('registration_date').aggregate(
        daily_registrations=lambda t: t.id.count()
    ).order_by('registration_date')