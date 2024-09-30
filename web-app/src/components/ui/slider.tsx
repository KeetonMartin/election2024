import * as React from "react"
import * as SliderPrimitive from "@radix-ui/react-slider"

import { cn } from "@/lib/utils"

const Slider = React.forwardRef<
  React.ElementRef<typeof SliderPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof SliderPrimitive.Root>
>(({ className, ...props }, ref) => (
  <SliderPrimitive.Root
    ref={ref}
    className={cn(
      "nrelative nflex nw-full ntouch-none nselect-none nitems-center",
      className
    )}
    {...props}
  >
    <SliderPrimitive.Track className="nrelative nh-2 nw-full ngrow noverflow-hidden nrounded-full nbg-secondary">
      <SliderPrimitive.Range className="nabsolute nh-full nbg-primary" />
    </SliderPrimitive.Track>
    <SliderPrimitive.Thumb className="nblock nh-5 nw-5 nrounded-full nborder-2 nborder-primary nbg-background nring-offset-background ntransition-colors focus-visible:noutline-none focus-visible:nring-2 focus-visible:nring-ring focus-visible:nring-offset-2 disabled:npointer-events-none disabled:nopacity-50" />
  </SliderPrimitive.Root>
))
Slider.displayName = SliderPrimitive.Root.displayName

export { Slider }
