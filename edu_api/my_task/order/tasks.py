import datetime

from my_task.main import app


@app.tasks(name="check_order")
def check_order():
    # 超时取消
    pass
