from datetime import datetime
import cv2, time, pandas, plotting

video = cv2.VideoCapture(0)

status_list = [None, None]
first_frame = None
times = []
while True:
    status = 0

    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) >= 10000:
            status = 1
            (x, y, width, height) =  cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+width,y+height), (0,255,0), 3)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())



    cv2.imshow("Gray Blurred Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if(key == ord('q')):
        if status == 1:
            times.append(datetime.now())
        break

df = pandas.DataFrame(columns=["Start", "End"])
for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

video.release()
cv2.destroyAllWindows()
plotting.show_motion_graph(df)
