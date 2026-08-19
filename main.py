from app.tools.data_tools import profile_csv

def main():
    result = profile_csv.invoke(
        {
            "file_path":"data/sales.csv"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
