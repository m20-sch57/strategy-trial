import a as summing;
def double_mult(a: int, b: int) -> int:
    return summing.summ(a, b) ** 2 - a ** 2 - b ** 2;

if __name__ == "__main__":
    a, b = map(int, input().split());
    print(double_mult(a, b));