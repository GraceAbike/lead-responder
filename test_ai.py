from app import crud


def main():
    customer_message = (
        "Hi, I need an emergency plumber to fix a leaking pipe under my kitchen sink today."
    )
    print("Customer request:")
    print(customer_message)
    print("\nGenerating AI response...\n")

    try:
        ai_response = crud.generate_ai_response(customer_message)
    except Exception as exc:
        print("ERROR: Could not generate AI response.")
        print(str(exc))
        return

    print("AI response:")
    print(ai_response)


if __name__ == "__main__":
    main()
