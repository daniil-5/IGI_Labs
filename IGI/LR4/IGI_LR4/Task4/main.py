from Task4.triangle import Triangle

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a positive number.")

def get_string_input(prompt):
    value = input(prompt).strip()
    if not value:
        print("Empty input. Try again.")
        return get_string_input(prompt)
    return value

def get_valid_color(prompt):
    from matplotlib.colors import CSS4_COLORS, TABLEAU_COLORS
    while True:
        color = input(prompt).strip().lower()
        if color in CSS4_COLORS or color in TABLEAU_COLORS:
            return color
        print("Invalid color name. Please enter a valid matplotlib color (e.g., 'blue', 'orange', 'cyan').")


def draw_triangle():
    print("Triangle Around Circle Figure Generator")
    radius = get_float_input("Enter circle radius R: ")
    color = get_valid_color("Enter figure color (e.g., 'red', 'blue'): ")
    label = get_string_input("Enter label text for figure: ")

    triangle = Triangle(radius, color)
    print(triangle.description())
    triangle.draw(label)

if __name__ == "__main__":
    draw_triangle()

