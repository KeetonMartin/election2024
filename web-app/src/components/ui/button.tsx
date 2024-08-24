import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "ninline-flex nitems-center njustify-center nwhitespace-nowrap nrounded-md ntext-sm nfont-medium nring-offset-background ntransition-colors focus-visible:noutline-none focus-visible:nring-2 focus-visible:nring-ring focus-visible:nring-offset-2 disabled:npointer-events-none disabled:nopacity-50",
  {
    variants: {
      variant: {
        default: "nbg-primary ntext-primary-foreground hover:nbg-primary/90",
        destructive:
          "nbg-destructive ntext-destructive-foreground hover:nbg-destructive/90",
        outline:
          "nborder nborder-input nbg-background hover:nbg-accent hover:ntext-accent-foreground",
        secondary:
          "nbg-secondary ntext-secondary-foreground hover:nbg-secondary/80",
        ghost: "hover:nbg-accent hover:ntext-accent-foreground",
        link: "ntext-primary nunderline-offset-4 hover:nunderline",
      },
      size: {
        default: "nh-10 npx-4 npy-2",
        sm: "nh-9 nrounded-md npx-3",
        lg: "nh-11 nrounded-md npx-8",
        icon: "nh-10 nw-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
