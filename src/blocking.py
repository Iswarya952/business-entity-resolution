import pandas as pd
import os


def create_block_key(name, country):
    name = str(name)
    country = str(country)

    if not name:
        return country

    first_token = name.split()[0]

    return country + "_" + first_token[:4]


def build_index(source_df):
    index = {}

    for _, row in source_df.iterrows():

        key = create_block_key(
            row["name_norm"],
            row["country_norm"]
        )

        if key not in index:
            index[key] = []

        index[key].append(row["entity_id"])

    return index


def generate_candidates(source1, source2, source3):

    index2 = build_index(source2)
    index3 = build_index(source3)

    results = []

    for _, row in source1.iterrows():

        key = create_block_key(
            row["name_norm"],
            row["country_norm"]
        )

        candidates = []

        candidates.extend(index2.get(key, []))
        candidates.extend(index3.get(key, []))

        candidates = list(dict.fromkeys(candidates))

        results.append({
            "source1_entity_id": row["entity_id"],
            "candidate_entity_ids": ",".join(candidates)
        })

    return pd.DataFrame(results)


def main():

    os.makedirs("output", exist_ok=True)

    source1 = pd.read_csv(
        "data/processed/train_source1_normalized.tsv",
        sep="\t"
    )

    source2 = pd.read_csv(
        "data/processed/train_source2_normalized.tsv",
        sep="\t"
    )

    source3 = pd.read_csv(
        "data/processed/train_source3_normalized.tsv",
        sep="\t"
    )

    candidates = generate_candidates(
        source1,
        source2,
        source3
    )

    candidates.to_csv(
        "output/candidate_pairs.tsv",
        sep="\t",
        index=False
    )

    print("Candidate generation completed.")
    print("Saved: output/candidate_pairs.tsv")


if __name__ == "__main__":
    main()