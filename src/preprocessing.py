import pandas as pd
import re
import unicodedata


def normalize_text(value):
    if pd.isna(value):
        return ""

    text = str(value)
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_country(value):
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def process_file(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t")

    df["name_norm"] = df["business_name"].map(normalize_text)
    df["address_norm"] = df["business_address"].map(normalize_text)
    df["country_norm"] = df["country"].map(normalize_country)

    df.to_csv(output_file, sep="\t", index=False)

    print("Completed:", input_file)
    print("Saved:", output_file)


def main():

    process_file(
        "data/train/train_source1.tsv",
        "data/processed/train_source1_normalized.tsv"
    )

    process_file(
        "data/train/train_source2.tsv",
        "data/processed/train_source2_normalized.tsv"
    )

    process_file(
        "data/train/train_source3.tsv",
        "data/processed/train_source3_normalized.tsv"
    )


if __name__ == "__main__":
    main()