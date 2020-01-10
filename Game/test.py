import cv2

def Mask(background = 'full.png', top = 'backg.png', mask = 'mask.png', img = None):
    # Read the images
    if img is not None:
        background = img
    else:
        background = cv2.imread(background)

    foreground = cv2.imread(top)
    alpha = cv2.imread(mask)

    # Convert uint8 to float
    #foreground = foreground.astype(float)
    #background = background.astype(float)

    # Normalize the alpha mask to keep intensity between 0 and 1
    #alpha = alpha.astype(float)/255

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - alpha, background)

    # Add the masked foreground and background.
    outImage = cv2.add(foreground, background)

    return outImage

# Display image
cv2.imshow("outImg", Mask()/255)
cv2.waitKey(0)
