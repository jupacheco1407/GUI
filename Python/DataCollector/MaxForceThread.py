from PySide6.QtCore import QThread, Signal

class MaxForceThread(QThread):
    # Declaração dos sinais
    progress_updated = Signal(int)  # Pode ser int, float, etc. Ajuste conforme seu progresso
    calculation_complete = Signal(float)  # Valor final do cálculo, por exemplo

    def __init__(self, base):
        super().__init__()
        self.base = base
        self._is_running = True

    def run(self):
        max_force = 0.0
        # Exemplo de loop de cálculo de força máxima
        for i in range(100):
            if not self._is_running:
                break
            # Simula cálculo ou leitura de dados
            # (substitua isso pela lógica real da sua aplicação)
            max_force = max(max_force, self.get_current_force())

            # Emite progresso como porcentagem (0 a 100)
            self.progress_updated.emit(i + 1)

            # Pequena pausa simulada (para não travar a thread)
            self.msleep(50)

        # Quando cálculo terminar, emite o resultado final
        self.calculation_complete.emit(max_force)

    def get_current_force(self):
        # Implementar a leitura/ cálculo real da força máxima
        # Aqui só um dummy para exemplo
        import random
        return random.uniform(0, 100)

    def stop(self):
        self._is_running = False
