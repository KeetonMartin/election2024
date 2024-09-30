import * as React from "react"
import * as SheetPrimitive from "@radix-ui/react-dialog"
import { cva, type VariantProps } from "class-variance-authority"
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const Sheet = SheetPrimitive.Root

const SheetTrigger = SheetPrimitive.Trigger

const SheetClose = SheetPrimitive.Close

const SheetPortal = SheetPrimitive.Portal

const SheetOverlay = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Overlay
    className={cn(
      "nfixed ninset-0 nz-50 nbg-black/80 n data-[state=open]:nanimate-in data-[state=closed]:nanimate-out data-[state=closed]:nfade-out-0 data-[state=open]:nfade-in-0",
      className
    )}
    {...props}
    ref={ref}
  />
))
SheetOverlay.displayName = SheetPrimitive.Overlay.displayName

const sheetVariants = cva(
  "nfixed nz-50 ngap-4 nbg-background np-6 nshadow-lg ntransition nease-in-out data-[state=open]:nanimate-in data-[state=closed]:nanimate-out data-[state=closed]:nduration-300 data-[state=open]:nduration-500",
  {
    variants: {
      side: {
        top: "ninset-x-0 ntop-0 nborder-b data-[state=closed]:nslide-out-to-top data-[state=open]:nslide-in-from-top",
        bottom:
          "ninset-x-0 nbottom-0 nborder-t data-[state=closed]:nslide-out-to-bottom data-[state=open]:nslide-in-from-bottom",
        left: "ninset-y-0 nleft-0 nh-full nw-3/4 nborder-r data-[state=closed]:nslide-out-to-left data-[state=open]:nslide-in-from-left sm:nmax-w-sm",
        right:
          "ninset-y-0 nright-0 nh-full nw-3/4 n nborder-l data-[state=closed]:nslide-out-to-right data-[state=open]:nslide-in-from-right sm:nmax-w-sm",
      },
    },
    defaultVariants: {
      side: "right",
    },
  }
)

interface SheetContentProps
  extends React.ComponentPropsWithoutRef<typeof SheetPrimitive.Content>,
    VariantProps<typeof sheetVariants> {}

const SheetContent = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Content>,
  SheetContentProps
>(({ side = "right", className, children, ...props }, ref) => (
  <SheetPortal>
    <SheetOverlay />
    <SheetPrimitive.Content
      ref={ref}
      className={cn(sheetVariants({ side }), className)}
      {...props}
    >
      {children}
      <SheetPrimitive.Close className="nabsolute nright-4 ntop-4 nrounded-sm nopacity-70 nring-offset-background ntransition-opacity hover:nopacity-100 focus:noutline-none focus:nring-2 focus:nring-ring focus:nring-offset-2 disabled:npointer-events-none data-[state=open]:nbg-secondary">
        <X className="nh-4 nw-4" />
        <span className="nsr-only">Close</span>
      </SheetPrimitive.Close>
    </SheetPrimitive.Content>
  </SheetPortal>
))
SheetContent.displayName = SheetPrimitive.Content.displayName

const SheetHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "nflex nflex-col nspace-y-2 ntext-center sm:ntext-left",
      className
    )}
    {...props}
  />
)
SheetHeader.displayName = "SheetHeader"

const SheetFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "nflex nflex-col-reverse sm:nflex-row sm:njustify-end sm:nspace-x-2",
      className
    )}
    {...props}
  />
)
SheetFooter.displayName = "SheetFooter"

const SheetTitle = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Title>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Title
    ref={ref}
    className={cn("ntext-lg nfont-semibold ntext-foreground", className)}
    {...props}
  />
))
SheetTitle.displayName = SheetPrimitive.Title.displayName

const SheetDescription = React.forwardRef<
  React.ElementRef<typeof SheetPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof SheetPrimitive.Description>
>(({ className, ...props }, ref) => (
  <SheetPrimitive.Description
    ref={ref}
    className={cn("ntext-sm ntext-muted-foreground", className)}
    {...props}
  />
))
SheetDescription.displayName = SheetPrimitive.Description.displayName

export {
  Sheet,
  SheetPortal,
  SheetOverlay,
  SheetTrigger,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetFooter,
  SheetTitle,
  SheetDescription,
}
