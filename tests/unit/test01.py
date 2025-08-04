current_mae = 222.0
new_mae = 220.0
improvement = (current_mae - new_mae) / current_mae
print(improvement)

threshold = 0.5
if improvement >= threshold:
    print(f"Modelo promocionado. Mejora del {improvement:.2f}%")
else:
    print(f"Modelo NO promocionado. Mejora del {improvement:.2f}%")
