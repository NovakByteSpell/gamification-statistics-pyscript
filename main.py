import pandas as pd
from typing import Dict, List, Any, Tuple
import numpy.typing as npt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def get_excel_data(index_name: str) -> npt.NDArray[Any]:
    df: pd.DataFrame = pd.read_excel("data.xlsx")
    return df[index_name].to_numpy()


def clean_data() -> Dict[str, npt.NDArray[Any]]:
    raw_teacher_knowledge: npt.NDArray[Any] = get_excel_data(
        "Vet du vad spelifiering/gamification är?"
    )
    teacher_knowledge: List[bool] = [i == "Ja" for i in raw_teacher_knowledge]

    excel_data: Dict[str, npt.NDArray[Any]] = {
        "time": get_excel_data("Timestamp"),
        "age": get_excel_data("Hur gammal är du?"),
        "gender": get_excel_data("Vad för könsidentitet har du?"),
        "time_exam": get_excel_data("När tog du lärarexamen?"),
        "primary_subject": get_excel_data(
            "Vilket är ditt primära undervisningsområde?"
        ),
        "teacher_awareness": np.array(teacher_knowledge),
        "implementation_attitude": get_excel_data(
            "Vad är din inställning till att implementera spelifiering/gamification i din undervisning? "
        ),
        "current_gamification_use": get_excel_data(
            "Hur mycket andvänder du spelifiering i din undervisning?"
        ),
        "gamification_usage_reason": get_excel_data(
            "Varför/varför inte andvänder du Spelifiering/Gamification i din undervisning "
        ),
        "feedback": get_excel_data(
            "Finns det en fråga som du upplever jag borde ta upp? Finns det en fråga du inte upplever att du förstod? Upplevde du att enkäten var för långa/kort? Din feedback är uppskattad."
        ),
    }
    return excel_data


def average(values: npt.NDArray[Any], filters: npt.NDArray[Any]) -> float:
    if len(values) != len(filters):
        return 0
    else:
        pass

    data_length: int = len(values)
    paired_data: List[Tuple[int, bool]] = [
        (values[i], filters[i]) for i in range(data_length)
    ]
    selected_values: List[int] = [val for val, condition in paired_data if condition]

    if not selected_values:
        return 0
    else:
        pass
    return sum(selected_values) / data_length


def main():
    excel_data = clean_data()

    avg_age_aware = average(excel_data["age"], excel_data["teacher_awareness"])
    # Average age of participants who knew what gamification was
    print(round(avg_age_aware))
    # Average age of the participants
    print(round(sum(excel_data["age"]) / len(excel_data["age"])))

    time_exam_dates = pd.to_datetime(excel_data["time_exam"])
    current_year = pd.Timestamp.now().year
    years_since_graduation = current_year - np.array([d.year for d in time_exam_dates])

    attitudes = excel_data["implementation_attitude"]

    slope, intercept, r_value, p_value, std_err = linregress(
        years_since_graduation, attitudes
    )

    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"Correlation (r): {r_value}")
    print(f"P-value: {p_value}")

    plt.scatter(years_since_graduation, attitudes)
    plt.plot(
        years_since_graduation, slope * years_since_graduation + intercept, color="red"
    )  # regression line
    plt.xlabel("Years Since Graduation")
    plt.ylabel("Attitude Toward Gamification")
    plt.title("Experience vs Attitude Toward Gamification")
    plt.show()


if __name__ == "__main__":
    main()
