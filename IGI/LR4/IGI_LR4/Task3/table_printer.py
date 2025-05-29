def print_table(data):
    """
    Prints formatted table of sin(x) approximation values.
    """
    print(f"{'x':^10} | {'n':^5} | {'F(x)':^15} | {'Math F(x)':^15} | {'eps':^15}")
    print("-" * 70)
    for row in data:
        print(f"{row['x']:^10.4f} | {row['n']:^5} | {row['F(x)']:^15.10f} | {row['Math F(x)']:^15.10f} | {row['eps']:^15.10f}")
