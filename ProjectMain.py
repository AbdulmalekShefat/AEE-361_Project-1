import Vector
import PrincipleStress
import Stress
import wx

# Example for stress input format: -19,-4.7,6.45/-4.7,4.6,11.8/6.45,11.8,-8.3
# Example for vector input format: 1,4,2

# List of the possible choices
choices = ['Vector Transformation', 'Stress Transformation', 'Principle Stress']


# Function to show dialog with selectable items
def choose(title='AEE 361 Project', label='Choose which transformation to make'):
    modal = wx.SingleChoiceDialog(None, label, title, choices)

    if modal.ShowModal() == wx.ID_OK:
        result = modal.GetStringSelection()
    else:
        result = "cancelled"
    modal.Destroy()
    return result


# Initialize the dialog interface
app = wx.App()
app.MainLoop()

# show the choices dialog
choice = choose()

# release the interface
app.ExitMainLoop()

# check for the choice
if choice == choices[0]:
    Vector.vector_main_()
elif choice == choices[1]:
    Stress.stress_main_()
elif choice == choices[2]:
    PrincipleStress.principle_stress_main()
