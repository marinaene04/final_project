# ============================================================
# COMPANY FINANCIAL HEALTH SCANNER
# Programming for Economists II - Final Project
# ============================================================
# This program reads company financial data from a text file,
# calculates key financial ratios, assigns a health grade
# (A through F), and generates a report saved to a file.
# The user can also input a company manually for instant analysis.
# ============================================================


# -------------------- DATA LOADING --------------------

def load_companies(filename):
    """
    Reads company financial data from a text file.
    Each line format: Name,Revenue,Costs,Debt,Cash,Employees
    :param filename: string, path to the data file
    :return: dictionary where keys are company names and
             values are dictionaries with financial data
    """
    companies = {}

    try:
        fp = open(filename, "r")
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found.")
        return companies

    for line in fp:
        line = line.strip()

        # Skip empty lines
        if len(line) == 0:
            continue

        parts = line.split(",")

        # We expect exactly 6 fields per line
        if len(parts) != 6:
            print("Warning: Skipping bad line ->", line)
            continue

        try:
            name = parts[0].strip()
            revenue = float(parts[1].strip())
            costs = float(parts[2].strip())
            debt = float(parts[3].strip())
            cash = float(parts[4].strip())
            employees = int(parts[5].strip())

            companies[name] = {
                "revenue": revenue,
                "costs": costs,
                "debt": debt,
                "cash": cash,
                "employees": employees
            }
        except ValueError:
            print("Warning: Invalid numbers in line ->", line)
            continue

    fp.close()
    print("Loaded", len(companies), "companies from", filename)
    return companies


# -------------------- RATIO CALCULATIONS --------------------

def calculate_profit_margin(revenue, costs):
    """
    Calculates profit margin as a percentage.
    Profit Margin = (Revenue - Costs) / Revenue * 100
    :param revenue: float, total revenue in millions
    :param costs: float, total costs in millions
    :return: float, profit margin percentage (can be negative)
    """
    if revenue == 0:
        return 0.0
    profit = revenue - costs
    margin = (profit / revenue) * 100
    return round(margin, 2)


def calculate_debt_to_revenue(debt, revenue):
    """
    Calculates the debt-to-revenue ratio as a percentage.
    Lower is better - means less debt relative to income.
    :param debt: float, total debt in millions
    :param revenue: float, total revenue in millions
    :return: float, debt-to-revenue percentage
    """
    if revenue == 0:
        return 999.99
    ratio = (debt / revenue) * 100
    return round(ratio, 2)


def calculate_cash_runway(cash, costs, revenue):
    """
    Estimates how many months the company can survive on cash alone.
    Cash Runway = Cash / Monthly Burn Rate
    Monthly burn = (Costs - Revenue) / 12 if losing money, else "infinite"
    :param cash: float, cash reserves in millions
    :param costs: float, total annual costs in millions
    :param revenue: float, total annual revenue in millions
    :return: float, months of runway (-1 means profitable, no burn)
    """
    monthly_burn = (costs - revenue) / 12

    # If the company is profitable, it is not burning cash
    if monthly_burn <= 0:
        return -1.0

    # If cash is zero or negative, runway is 0
    if cash <= 0:
        return 0.0

    runway = cash / monthly_burn
    return round(runway, 1)


def calculate_revenue_per_employee(revenue, employees):
    """
    Calculates revenue generated per employee (efficiency metric).
    :param revenue: float, total revenue in millions
    :param employees: int, number of employees
    :return: float, revenue per employee in millions
    """
    if employees == 0:
        return 0.0
    rpe = revenue / employees
    return round(rpe, 2)


# -------------------- GRADING SYSTEM --------------------

def assign_grade(profit_margin, debt_ratio, cash_runway):
    """
    Assigns a health grade (A through F) based on financial ratios.
    Uses a point system: each metric earns 0-3 points.
    Total points determine the final grade.
    :param profit_margin: float, profit margin percentage
    :param debt_ratio: float, debt-to-revenue percentage
    :param cash_runway: float, months of cash runway (-1 = profitable)
    :return: tuple of (grade string, total points integer)
    """
    points = 0

    # --- Score profit margin (0 to 3 points) ---
    if profit_margin >= 20:
        points = points + 3
    elif profit_margin >= 10:
        points = points + 2
    elif profit_margin >= 0:
        points = points + 1
    else:
        points = points + 0  # Negative margin = 0 points

    # --- Score debt ratio (0 to 3 points) ---
    if debt_ratio <= 20:
        points = points + 3
    elif debt_ratio <= 40:
        points = points + 2
    elif debt_ratio <= 70:
        points = points + 1
    else:
        points = points + 0  # Very high debt = 0 points

    # --- Score cash runway (0 to 3 points) ---
    if cash_runway == -1.0:
        # Profitable company, no burn
        points = points + 3
    elif cash_runway >= 18:
        points = points + 2
    elif cash_runway >= 6:
        points = points + 1
    else:
        points = points + 0  # Less than 6 months = danger

    # --- Convert total points to a letter grade ---
    if points >= 8:
        grade = "A"
    elif points >= 6:
        grade = "B"
    elif points >= 4:
        grade = "C"
    elif points >= 2:
        grade = "D"
    else:
        grade = "F"

    return (grade, points)


# -------------------- ANALYSIS ENGINE --------------------

def analyze_company(name, data):
    """
    Runs the full financial analysis on one company.
    Calculates all ratios and assigns a grade.
    :param name: string, company name
    :param data: dictionary with keys: revenue, costs, debt, cash, employees
    :return: dictionary with all calculated metrics and grade
    """
    revenue = data["revenue"]
    costs = data["costs"]
    debt = data["debt"]
    cash = data["cash"]
    employees = data["employees"]

    profit_margin = calculate_profit_margin(revenue, costs)
    debt_ratio = calculate_debt_to_revenue(debt, revenue)
    cash_runway = calculate_cash_runway(cash, costs, revenue)
    rev_per_emp = calculate_revenue_per_employee(revenue, employees)

    grade_info = assign_grade(profit_margin, debt_ratio, cash_runway)

    result = {
        "name": name,
        "revenue": revenue,
        "costs": costs,
        "profit_margin": profit_margin,
        "debt_ratio": debt_ratio,
        "cash_runway": cash_runway,
        "rev_per_employee": rev_per_emp,
        "grade": grade_info[0],
        "points": grade_info[1]
    }

    return result


def analyze_all_companies(companies):
    """
    Runs analysis on every company in the dictionary.
    :param companies: dictionary of company data (from load_companies)
    :return: list of result dictionaries (one per company)
    """
    results = []

    for name in companies:
        data = companies[name]
        result = analyze_company(name, data)
        results.append(result)

    return results


# -------------------- DISPLAY FUNCTIONS --------------------

def display_result(result):
    """
    Prints the analysis result for one company in a readable format.
    :param result: dictionary with calculated metrics
    :return: None (prints to screen)
    """
    print("")
    print("=" * 50)
    print("  COMPANY: " + result["name"])
    print("=" * 50)
    print(f"  Revenue:            ${result['revenue']:,.0f}M")
    print(f"  Costs:              ${result['costs']:,.0f}M")
    print(f"  Profit Margin:      {result['profit_margin']}%")
    print(f"  Debt-to-Revenue:    {result['debt_ratio']}%")

    if result["cash_runway"] == -1.0:
        print("  Cash Runway:        Profitable (no burn)")
    else:
        print(f"  Cash Runway:        {result['cash_runway']} months")

    print(f"  Revenue/Employee:   ${result['rev_per_employee']}M")
    print("-" * 50)
    print(f"  HEALTH GRADE:       {result['grade']}  ({result['points']}/9 points)")
    print("=" * 50)


def display_ranking(results):
    """
    Displays all companies ranked by their health grade points.
    Uses a simple sorting approach with nested loops (bubble sort).
    :param results: list of result dictionaries
    :return: None (prints to screen)
    """
    # Make a copy so we don't change the original list
    sorted_results = []
    for r in results:
        sorted_results.append(r)

    # Simple bubble sort by points (highest first)
    for i in range(len(sorted_results)):
        for j in range(i + 1, len(sorted_results)):
            if sorted_results[j]["points"] > sorted_results[i]["points"]:
                temp = sorted_results[i]
                sorted_results[i] = sorted_results[j]
                sorted_results[j] = temp

    print("")
    print("=" * 55)
    print("       FINANCIAL HEALTH RANKING")
    print("=" * 55)
    print(f"  {'Rank':<6}{'Company':<15}{'Grade':<8}{'Points':<10}{'Margin'}")
    print("-" * 55)

    rank = 1
    for r in sorted_results:
        print(f"  {rank:<6}{r['name']:<15}{r['grade']:<8}{r['points']}/9{'':<6}{r['profit_margin']}%")
        rank = rank + 1

    print("=" * 55)


# -------------------- REPORT GENERATION --------------------

def save_report(results, filename):
    """
    Writes the full analysis report to a text file.
    :param results: list of result dictionaries
    :param filename: string, output file path
    :return: True if successful, False if error
    """
    try:
        fp = open(filename, "w")
    except:
        print("Error: Could not create report file.")
        return False

    fp.write("COMPANY FINANCIAL HEALTH REPORT\n")
    fp.write("=" * 50 + "\n\n")

    for r in results:
        fp.write("Company: " + r["name"] + "\n")
        fp.write(f"  Revenue:          ${r['revenue']:,.0f}M\n")
        fp.write(f"  Profit Margin:    {r['profit_margin']}%\n")
        fp.write(f"  Debt-to-Revenue:  {r['debt_ratio']}%\n")

        if r["cash_runway"] == -1.0:
            fp.write("  Cash Runway:      Profitable (no burn)\n")
        else:
            fp.write(f"  Cash Runway:      {r['cash_runway']} months\n")

        fp.write(f"  Rev/Employee:     ${r['rev_per_employee']}M\n")
        fp.write(f"  GRADE:            {r['grade']} ({r['points']}/9)\n")
        fp.write("-" * 50 + "\n\n")

    fp.write("END OF REPORT\n")
    fp.close()
    print("Report saved to:", filename)
    return True


# -------------------- INTERACTIVE INPUT --------------------

def get_company_from_user():
    """
    Asks the user to input financial data for a single company.
    Uses try/except for input validation.
    :return: tuple of (name string, data dictionary) or None if cancelled
    """
    print("\n--- Enter Company Financial Data ---")
    name = input("Company name (or 'quit' to cancel): ").strip()

    if name.lower() == "quit" or len(name) == 0:
        return None

    # Validate each numeric input with a while loop + try/except
    revenue = get_valid_number("Revenue (in millions): ")
    costs = get_valid_number("Costs (in millions): ")
    debt = get_valid_number("Total Debt (in millions): ")
    cash = get_valid_number("Cash Reserves (in millions): ")
    employees = get_valid_integer("Number of Employees: ")

    data = {
        "revenue": revenue,
        "costs": costs,
        "debt": debt,
        "cash": cash,
        "employees": employees
    }

    return (name, data)


def get_valid_number(prompt):
    """
    Keeps asking until the user enters a valid float number.
    :param prompt: string, the message to display
    :return: float, the validated number
    """
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_valid_integer(prompt):
    """
    Keeps asking until the user enters a valid integer.
    :param prompt: string, the message to display
    :return: int, the validated integer
    """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("  Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# -------------------- MAIN MENU --------------------

def show_menu():
    """
    Displays the main menu options.
    :return: None
    """
    print("\n" + "=" * 45)
    print("  FINANCIAL HEALTH SCANNER - MAIN MENU")
    print("=" * 45)
    print("  1. Load & analyze companies from file")
    print("  2. Enter a company manually")
    print("  3. View ranking of loaded companies")
    print("  4. Save report to file")
    print("  5. Exit")
    print("=" * 45)


def main():
    """
    Main function that runs the program loop.
    Controls the menu and calls other functions.
    :return: None
    """
    print("\n" + "*" * 50)
    print("  Welcome to the Financial Health Scanner!")
    print("  Analyze any company's financial health.")
    print("*" * 50)

    # This list will store all analysis results
    all_results = []
    companies = {}

    while True:
        show_menu()
        choice = input("  Choose an option (1-5): ").strip()

        if choice == "1":
            # Load companies from file
            filename = input("  Enter filename (default: companies.txt): ").strip()
            if len(filename) == 0:
                filename = "companies.txt"

            companies = load_companies(filename)

            if len(companies) > 0:
                all_results = analyze_all_companies(companies)
                print("\nAnalysis complete! Here are the results:\n")
                for result in all_results:
                    display_result(result)

        elif choice == "2":
            # Manual company entry
            user_input = get_company_from_user()

            if user_input is not None:
                name = user_input[0]
                data = user_input[1]
                result = analyze_company(name, data)
                display_result(result)
                all_results.append(result)
                print("  (Company added to current session)")

        elif choice == "3":
            # Show ranking
            if len(all_results) == 0:
                print("\n  No companies loaded yet. Use option 1 or 2 first.")
            else:
                display_ranking(all_results)

        elif choice == "4":
            # Save report
            if len(all_results) == 0:
                print("\n  No companies to report. Use option 1 or 2 first.")
            else:
                out_file = input("  Report filename (default: report.txt): ").strip()
                if len(out_file) == 0:
                    out_file = "report.txt"
                save_report(all_results, out_file)

        elif choice == "5":
            print("\n  Thank you for using Financial Health Scanner!")
            print("  Goodbye!\n")
            break

        else:
            print("\n  Invalid choice. Please enter 1, 2, 3, 4, or 5.")


# -------------------- RUN THE PROGRAM --------------------
main()
