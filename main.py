from itertools import combinations


def optimize_cutting(required_lengths, stock_length):

    # Remove pieces longer than stock length
    valid_pieces = [l for l in required_lengths if l <= stock_length]
    if len(valid_pieces) != len(required_lengths):
        print("Warning: Some pieces exceed stock length and were ignored")

    # Sort pieces in descending order for better packing
    valid_pieces.sort(reverse=True)

    patterns = []
    remaining_pieces = valid_pieces.copy()

    while remaining_pieces:
        current_pattern = []
        remaining_length = stock_length

        # Try to find the best combination
        for i in range(len(remaining_pieces), 0, -1):
            found = False
            # Check all combinations of i pieces
            for combo in combinations(remaining_pieces, i):
                if sum(combo) <= stock_length:
                    # Find the combination that leaves least waste
                    if (stock_length - sum(combo)) < remaining_length:
                        remaining_length = stock_length - sum(combo)
                        best_combo = combo
                        found = True

            if found:
                # Add this combination to the pattern
                current_pattern = list(best_combo)
                # Remove used pieces from remaining pieces
                for piece in best_combo:
                    remaining_pieces.remove(piece)
                break

        if not current_pattern:
            # Add the largest remaining piece if no combination found
            piece = remaining_pieces.pop(0)
            current_pattern = [piece]
            remaining_length = stock_length - piece

        patterns.append({
            'pieces': current_pattern,
            'waste': remaining_length,
            'used_length': stock_length - remaining_length
        })

    # Calculate statistics
    total_waste = sum(p['waste'] for p in patterns)
    total_used = sum(p['used_length'] for p in patterns)
    efficiency = (total_used / (total_used + total_waste)) * 100

    return {
        'patterns': patterns,
        'total_stock_used': len(patterns),
        'total_waste': total_waste,
        'total_used': total_used,
        'efficiency': efficiency
    }


def get_user_input():
    """Get required pieces from user input"""
    print("Enter the lengths of required pieces (in meters).")
    print("Enter one value at a time. Press Enter with no input to finish.")

    pieces = []
    while True:
        piece = input(f"Piece {len(pieces) + 1}: ")
        if piece == "":
            break
        try:
            pieces.append(float(piece))
        except ValueError:
            print("Please enter a valid number")

    return pieces


def main():
    # Get required pieces from user
    print("+━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━>>>>>   CUTTING OPTIMIZER   <<<<<━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━+")
    print("│Ver 1.0, June-2025, by Nima.Z.Parsa                                                                                                │")
    print("│This is an executable portable program for calculating the cutting of steel profiles to minimize waste. This can be used           │\n"
          "│for Profile Section cuttings in construction sites, rebar cuttings for any reinforced concrete works and any similar industry.     │\n"
          "│This program is requested by my great friend eng.Kianoosh Pedrood.                                                                 │")
    print("+━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━+")
    stock_length = float(input("Enter the stock length (12m default): ") or 12)
    required_pieces = get_user_input()
    print("\n1- CHECKING")
    print("Required pieces:", required_pieces)
    print("Optimizing cutting for ",stock_length,"m steel profiles...\n")

    result = optimize_cutting(required_pieces, stock_length)

    print("\n2- CUTTING PLAN")
    print(f"Optimal cutting patterns (using {result['total_stock_used']} stock pieces):")
    for i, pattern in enumerate(result['patterns'], 1):
        print(f"Pattern {i}: {pattern['pieces']} (Used: {pattern['used_length']:.2f}m, Waste: {pattern['waste']:.2f}m)")

    print("\n3- REMAINED RESULT")
    print(f"Total waste: {result['total_waste']:.2f}m")
    print(f"Material efficiency: {result['efficiency']:.2f}%")


if __name__ == "__main__":
    main()