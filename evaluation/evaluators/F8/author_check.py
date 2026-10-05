"""Local ORIGINAL AUTHOR FIXTURE checks only. Not a model-submission execution switch."""
import argparse
import json
from grade import grade_author_fixture

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--submission",required=True)
    parser.add_argument("--runner",required=True)
    args=parser.parse_args()
    print(json.dumps(grade_author_fixture(args.submission,args.runner),ensure_ascii=False,indent=2))
