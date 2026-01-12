import math

def calculate_z_factor(ppr, tpr, gamma, tol=1e-6, max_iter=100):
    rho = 0.1
    Theta = 1 / tpr
    Alpha = 0.06125 * Theta * math.exp(-1.2 * (1 - Theta) ** 2)

    for _ in range(max_iter):
        f1 = -Alpha * ppr + ((rho + rho**2 + rho**3 - rho**4) / ((1 - rho) ** 3))
        f2 = -(14.76 * Theta - 9.76 * Theta**2 + 4.58 * Theta**3) * rho**2
        f3 = (90.7 * Theta - 242.2 * Theta**2 + 42.4 * Theta**3) * (
            rho ** (2.18 + 2.82 * Theta)
        )
        f = f1 + f2 + f3

        df1 = (1 + 4 * rho + 4 * rho**2 - 4 * rho**3 + rho**4) / ((1 - rho) ** 4)
        df2 = -(29.52 * Theta - 19.52 * Theta**2 + 9.16 * Theta**3) * rho
        df3 = (2.18 + 2.82 * Theta) * (90.7 * Theta - 242.2 * Theta**2 + 42.4 * Theta**3) * (
            rho ** (1.18 + 2.82 * Theta)
        )

        rho_new = rho - f / (df1 + df2 + df3)
        if abs(rho_new - rho) < tol:
            break
        rho = rho_new

    return Alpha * ppr / rho

