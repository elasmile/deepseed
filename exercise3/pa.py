import re

# List of common passwords (add more if needed)
common_passwords = [
    "123456", "password", "12345678", "qwerty", "abc123",
    "football", "123456789", "12345", "1234", "111111",
    "1234567", "dragon", "123123", "baseball", "letmein",
    "monkey", "696969", "shadow", "master", "superman",
    "passw0rd", "mypassword", "123qwe", "iloveyou"
]

def analyze_password(password):
    score = 0
    suggestions = []
    results = []

    # Criterion 1: Length
    if len(password) >= 8:
        score += 20
        results.append("✅ Length requirement (8+ chars)")
    else:
        results.append("❌ Too short (minimum 8 characters)")
        suggestions.append("- Use at least 8 characters")

    # Criterion 2: Uppercase
    if any(c.isupper() for c in password):
        score += 20
        results.append("✅ Contains uppercase letters")
    else:
        results.append("❌ No uppercase letters")
        suggestions.append("- Add some uppercase letters")

    # Criterion 3: Lowercase
    if any(c.islower() for c in password):
        score += 20
        results.append("✅ Contains lowercase letters")
    else:
        results.append("❌ No lowercase letters")
        suggestions.append("- Add some lowercase letters")

    # Criterion 4: Numbers
    if any(c.isdigit() for c in password):
        score += 20
        results.append("✅ Contains numbers")
    else:
        results.append("❌ No numbers included")
        suggestions.append("- Add digits (0-9)")

    # Criterion 5: Special Characters
    if re.search(r"[!@#$%^&*]", password):
        score += 20
        results.append("✅ Contains special characters")
    else:
        results.append("❌ Missing special characters (!@#$%^&*)")
        suggestions.append("- Include special characters (!@#$%^&*)")

    # Criterion 6: Not a common password
    if password.lower() in common_passwords:
        results.append("❌ Common password detected")
        suggestions.append("- Avoid common password patterns")
    else:
        score += 20
        results.append("✅ Not a common password")

    return score, results, suggestions

def strength_level(score):
    if score <= 40:
        return "Weak"
    elif score <= 60:
        return "Fair"
    elif score <= 80:
        return "Good"
    elif score <= 100:
        return "Strong"
    else:
        return "Excellent"

def main():
    print("=== PASSWORD SECURITY ANALYZER ===")
    password = input("Enter password to analyze: ")

    print("\n🔒 SECURITY ANALYSIS RESULTS")
    print(f"Password: {password}")

    score, results, suggestions = analyze_password(password)
    level = strength_level(score)

    print(f"Score: {score}/120 ({level})\n")
    for line in results:
        print(line)

    if suggestions:
        print("\n💡 SUGGESTIONS:")
        for s in suggestions:
            print(s)
    else:
        print("\n✅ Your password meets all security recommendations.")

if __name__ == "__main__":
    main()
