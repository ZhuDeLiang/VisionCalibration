import cv2

# 加载图片
img = cv2.imread('20_20005.jpg')
# 标注躺在床上的人
cv2.rectangle(img, (50, 100), (400, 300), (255, 0, 0), 2)
cv2.putText(img, 'Person', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

# 标注床
cv2.rectangle(img, (30, 50), (450, 350), (0, 255, 0), 2)
cv2.putText(img, 'Bed', (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# 标注输液架
cv2.rectangle(img, (470, 50), (510, 300), (0, 0, 255), 2)
cv2.putText(img, 'IV Stand', (470, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

# 标注输液瓶
cv2.rectangle(img, (475, 10), (500, 50), (255, 255, 0), 2)
cv2.putText(img, 'IV Bottle', (475, 0), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

# 标注门
cv2.rectangle(img, (200, 300), (600, 500), (255, 0, 255), 2)
cv2.putText(img, 'Door', (200, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
# 显示图片
cv2.imshow('Annotated Image', img)
cv2.waitKey(0)

# 保存图片
cv2.imwrite('annotated_image.jpg', img)
