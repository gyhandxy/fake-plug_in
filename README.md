# fake_plug_in
要修改Matrix.py中
“def __init__(self, raw : np.ndarray)"
改为
" @staticmethod
    def from2dArray(raw : np.ndarray):
        self.Rows = len(raw)
        self.Cols = len(raw[0])
        self.Vals = np.zeros((self.Rows, self.Cols))
        for i in range(self.Rows):
            for j in  range(self.Cols):
                self.Vals[i][j] = raw[i][j]
        return self"
 Python竟然不让函数重载
