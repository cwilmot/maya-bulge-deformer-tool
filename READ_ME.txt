Maya Bulge Deformer Tool!
Corey Wilmot


INSTALLATION:

1. Start up Maya.
2. Open the Script Editor.
3. Make sure the Python tab is clicked on in the editor.
4. Load in the MayaBulgeTool.py Python file from wherever you have it saved on your machine.
5. Once the file is loaded, click the Save Script to Shelf button at the top of the editor and name it something like "BulgeTool".
6. We now have a shelf button to activate our tool when needed.  Click on it and deform objects as you like! :D


FEATURES:

(Copy to Origin)- Select and duplicate an object in the scene.  The duplicate, if composed of multiple objects, will be combined
	into one piece of geometry.  The pivot position is now moved to the bottom center point of the object.
	The object is then moved to the origin, where it will have its transformations frozen and history deleted.
	
(Apply Bottom Bulge) - With a single piece of geometry selected, two non-linear bend deformers are applied to the base
	of the geometry.  With the help of X-axis and Z-axis curvature sliders, you can control the bulge amount from the
	bottom of the geometry.  Note: You can only bulge one piece of geo at a time.  Delete the objects history first before moving on.
	
(Create World Surface) - Allows the user to make a spherical surface under the origin to help them better gauge how much
	they would need to bulge their geometry to conform to a curved surface.  The World Scale slider allows to quickly change
	the degree of curvature of the surface.  It's essentially a fast proxy guide.
	
(Delete Construction History) - An easy access button to delete the history on an object.  You'll need to delete the history after
	the bottom bulge is applied before the object is exported out.  You also need to delete the history on an object before you
	move on to bulging another object.