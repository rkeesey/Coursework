from simpleimage import SimpleImage

def grayscale(image):
    
    copy_img = image.copy()

    for pixel in copy_img:
        red_0 = pixel.red
        green_0 = pixel.green
        blue_0 = pixel.blue

        sum_0 = red_0 + green_0 + blue_0
        avg = sum_0/3
         
        pixel.red = avg
        pixel.green = avg
        pixel.blue = avg

    return copy_img

def sepia(image):
    
    copy_img = image.copy()

    for pixel in copy_img:
        red_0 = pixel.red
        green_0 = pixel.green
        blue_0 = pixel.blue

        red_1 = 0.393*red_0 + 0.769*green_0 + 0.189*blue_0
        green_1 = 0.349*red_0 + 0.686*green_0 + 0.168*blue_0
        blue_1 = 0.272*red_0 + 0.534*green_0 + 0.131*blue_0
        
        pixel.red = red_1
        pixel.green = green_1
        pixel.blue = blue_1

    return copy_img

def shrink(image, scale):

    copy_img = image.copy()

    w = copy_img._width
    h = copy_img._height

    sh_w = w // scale
    sh_h = h // scale

    new_img = SimpleImage.blank(sh_w, sh_h)

    for x in range(sh_w):
        x_idx = x * scale
        for y in range(sh_h):
            y_idx = y * scale

            pixel = copy_img.get_pixel(x_idx, y_idx)
            new_img.set_pixel(x, y, pixel)

    return new_img

def mirror(image, direction):
    
    copy_img = image.copy()

    w = copy_img._width
    h = copy_img._height

    d_w = w * 2
    d_h = h * 2

    if direction == 0:
        new_img = SimpleImage.blank(d_w, h)
        img_x = d_w
        img_y = h

    elif direction == 1:
        new_img = SimpleImage.blank(w, d_h)
        img_x = w
        img_y = d_h

    for i in range(w):
        for j in range(h):
            pixel = copy_img.get_pixel(i, j)
            new_img.set_pixel(i, j, pixel)
            if direction == 0:
                new_img.set_pixel(img_x - i - 1, j, pixel)
            elif direction == 1:
                new_img.set_pixel(i, img_y - j - 1, pixel)

    return new_img
    
def blur(image):
    
    copy_img = image.copy()

    w = copy_img._width
    h = copy_img._height 

    for i in range(1, w - 1):
        for j in range(1,  h - 1):

            r_sum = 0
            g_sum = 0
            b_sum = 0 

            for x_block in range(i-1, i+2): 
                for y_block in range(j-1, j+2):
                    pixel = image.get_pixel(x_block, y_block)
                    r_sum += pixel.red
                    g_sum += pixel.green
                    b_sum += pixel.blue
            r_avg = r_sum/9
            g_avg = g_sum/9
            b_avg = b_sum/9

            new_pixel = copy_img.get_pixel(i, j)
            new_pixel.red = r_avg
            new_pixel.green = g_avg
            new_pixel.blue = b_avg

    return copy_img

def filter(image, channel, intensity):
    
    copy_img = image.copy()
    
    for pixel in copy_img:

        if channel == 'red':
            color = pixel.red
        elif channel == 'green':
            color = pixel.green
        elif channel == 'blue':
            color = pixel.blue

        red_0 = pixel.red
        green_0 = pixel.green
        blue_0 = pixel.blue

        sum_0 = red_0 + green_0 + blue_0
        avg = sum_0/3
        
        if color > intensity:
            continue
        else:
            pixel.red = avg
            pixel.green = avg
            pixel.blue = avg
    
    return copy_img
        
        
    
        

if __name__=='__main__':
    
    image = SimpleImage("yosemite.jpg")
    scale = 2
    channel = 'green'
    intensity = 150
    
    image.show()

    #grey = grayscale(image)
    #grey.show()

    #sep = sepia(image)
    #sep.show()

    #shrnk = shrink(image, scale)
    #shrnk.show()

    #mirr_0 = mirror(image, 0)
    #mirr_0.show()

    #mirr_1 = mirror(image, 1)
    #mirr_1.show()

    #blr = blur(image)
    #blr.show()

    fil = filter(image, channel, intensity)
    fil.show()
    
    