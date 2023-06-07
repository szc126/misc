// mirror and rotate an X11 window
// authored by Bing Chat (ChatGPT) and ChatGPT
// gcc main.c -lX11 -o main; ./main $window_id

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <stdio.h>
#include <stdlib.h>
#include <X11/extensions/sync.h>

// A function that rotates an image data by 90 degrees clockwise
void rotate_image(XImage *src, XImage *dst) {
  int x, y;
  for (x = 0; x < src->width; x++) {
    for (y = 0; y < src->height; y++) {
      // Copy the pixel value from (x,y) in src to (height-y-1,x) in dst
      XPutPixel(dst, src->height - y - 1, x, XGetPixel(src, x, y));
    }
  }
}

int main(int argc, char *argv[]) {
  Display *dpy; // The display connection
  Window root; // The root window
  Window win; // The original window
  Window mir; // The mirrored window
  GC gc; // The graphics context
  XImage *img; // The image of the original window
  XImage *rot; // The rotated image of the original window
  int width, height; // The width and height of the original window

  // Check if a window id is given as argument
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <window_id>\n", argv[0]);
    exit(1);
  }

  // Open the display connection
  dpy = XOpenDisplay(NULL);
  if (!dpy) {
    fprintf(stderr, "Cannot open display\n");
    exit(1);
  }

  // Get the root window
  root = DefaultRootWindow(dpy);

  // Get the original window from the argument
  win = (Window)strtol(argv[1], NULL, 0);

  // Get the width and height of the original window
  XWindowAttributes attr;
  XGetWindowAttributes(dpy, win, &attr);
  width = attr.width;
  height = attr.height;

  // Create a new window with swapped width and height
  mir = XCreateSimpleWindow(dpy, root, 0, 0, height, width,
                            0, BlackPixel(dpy, DefaultScreen(dpy)),
                            WhitePixel(dpy, DefaultScreen(dpy)));

  // Create a graphics context for drawing on the new window
  gc = XCreateGC(dpy, mir, 0, NULL);

  // Map the new window on the screen
  XMapWindow(dpy, mir);

  // Create an empty image with swapped width and height
  rot = XCreateImage(dpy, DefaultVisual(dpy, DefaultScreen(dpy)),
                     DefaultDepth(dpy, DefaultScreen(dpy)), ZPixmap,
                     0, NULL, height, width, 32, 0);

  // Allocate memory for the rotated image data
  rot->data = malloc(rot->bytes_per_line * rot->height);






/*
// A loop to update the mirrored window
while (1) {
  // Get the image from the original window
  img = XGetImage(dpy, win, 0, 0, width, height, AllPlanes, ZPixmap);

  // Rotate the image by 90 degrees
  rotate_image(img, rot);

  // Put the rotated image on the new window
  XPutImage(dpy, mir, gc, rot, 0, 0, 0, 0, height, width);

  // Free the image data
  XDestroyImage(img);

  // Flush the output buffer
  XFlush(dpy);

  // Check for a key press event without waiting
  XEvent event;
  if (XCheckMaskEvent(dpy, KeyPressMask, &event)) {
    break;
  }
}
*/



// Define the desired frames per second
const int FPS = 10;

// Calculate the time interval between frames
const int FRAME_TIME = 1000 / FPS;

// Get the current time in milliseconds
struct timeval t;
gettimeofday(&t, NULL);
long long prev_time = t.tv_sec * 1000LL + t.tv_usec / 1000LL;

while (1) {
  // Get the current time in milliseconds
  gettimeofday(&t, NULL);
  long long curr_time = t.tv_sec * 1000LL + t.tv_usec / 1000LL;

  // Calculate the time elapsed since the last frame
  long long elapsed_time = curr_time - prev_time;

  // If enough time has passed, update the frame
  if (elapsed_time >= FRAME_TIME) {
    // Get the image from the original window
    img = XGetImage(dpy, win, 0, 0, width, height, AllPlanes, ZPixmap);

    // Rotate the image by 90 degrees
    rotate_image(img, rot);

    // Put the rotated image on the new window
    XPutImage(dpy, mir, gc, rot, 0, 0, 0, 0, height, width);

    // Free the image data
    XDestroyImage(img);

    // Flush the output buffer
    XFlush(dpy);

    // Check for a key press event without waiting
    XEvent event;
    if (XCheckMaskEvent(dpy, KeyPressMask, &event)) {
      break;
    }

    // Update the previous time to the current time
    prev_time = curr_time;
  }
}







// Free the rotated image data
free(rot->data);

// Close the display connection
XCloseDisplay(dpy);

return 0;
}