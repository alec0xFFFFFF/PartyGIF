# Party Gif

From this

![Alt Text](assets/gator.png)

To this

![Alt Text](assets/gator.gif)


calculating size of gif

(x * y * fps * length) / 8 = size in bytes then compression
The GIF image format uses LZW compression. Infamous for the owner of the algorithm patent, Unisys, aggressively pursuing royalty payments just as the image format got popular. Turned out well, we got PNG to thank for that.

The amount by which LZW can compress the image is extremely non-deterministic and greatly depends on the image content. You, at best, can provide the user with a heuristic that estimates the final image file size. Displaying, say, a success prediction with a colored bar. You'd can color it pretty quickly by converting just the first frame. That won't take long on 384x216 image, that runs in human time, a fraction of a second.

And then extrapolate the effective compression rate of that first image to the subsequent frames. Which ought to encode only small differences from the original frame so ought to have comparable compression rates.

You can't truly know whether it exceeds the site's size limit until you've encoded the entire sequence. So be sure to emphasize in your UI design that your prediction is just an estimate so your user isn't going to disappointed too much. And of course provide him with the tools to get the size lowered, something like a nearest-neighbor interpolation that makes the pixels in the image bigger. Focusing on making the later frames smaller can pay off handsomely as well, GIF encoders don't normally do this well by themselves. YMMV.