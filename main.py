



while (pronpt := input("Enter a prompt (q to quit)")) != "q":
    result = rag.query(prompt)
    print(result.content)