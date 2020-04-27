from SerialDataVisualization.SerialCOMViewer import SerialCOMViewer


if __name__ == '__main__':
    app = SerialCOMViewer()
    app.geometry("480x720")
    app.mainloop()