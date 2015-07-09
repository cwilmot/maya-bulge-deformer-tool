# Corey Wilmot
# Bulge Tool
# 3-23-2015

import maya.cmds as cmds
import math

class Bulge_Window( object ):
    def __init__( self ):
        self.window = None
        self.window_name = 'bulge_window'
        self.title = "Bottom-Up Bulge Deformer"
        self.width = 250
        self.height = 300


    # Initialize new window, delete old one if it already exists
    def create(self):
        self.destroy()
        self.window = cmds.window(
            self.window_name       ,
            title    = self.title  ,
            width    = self.width  ,
            height   = self.height ,
            mnb      = False       ,
            mxb      = False       ,
            sizeable = False
            )
        
        # Add elements in the window
        self.create_common_buttons()
        
        cmds.showWindow()


    def destroy( self ):
        if cmds.window( self.window_name, exists=True ):
            cmds.deleteUI( self.window_name, window=True )


    # Initialize buttons
    def create_common_buttons( self ):
        cmds.setParent("..")
        cmds.columnLayout( adj=True, columnAlign="center" )
        cmds.separator( height=10, style="none" )

        cmds.text( label="Select one or more objects\nto be combined and moved to the origin." )
        cmds.separator( height=5, style="none" )
        self.button_duplicate = cmds.button( label="Copy to Origin", width=150, command=self.duplicate_button )
        cmds.separator( height=25, style="none" )

        cmds.text( label="Click to apply the bulge at the base of the geometry\nand adjust the sliders to control the bulginess." )
        cmds.separator( height=5, style="none" )
        self.button_bulge = cmds.button( label="Apply Bottom Bulge", width=150, command=self.bulge_button )
        cmds.separator( height=10, style="none" )
        cmds.intSliderGrp( "x_bulge_slider", label="X-axis Curvature", min=0, max=180, fieldMaxValue=180, field=True, value=0 )
        cmds.intSliderGrp( "z_bulge_slider", label="Z-axis Curvature", min=0, max=180, fieldMaxValue=180, field=True, value=0 )
        cmds.separator( height=25, style="none" )

        cmds.text( label="Option to create a spherical surface to help\nalign the curvature of the object." )
        cmds.separator( height=5, style="none" )
        self.button_create_world = cmds.button( label="Create World Surface", width=150, command=self.create_world_button )
        cmds.intSliderGrp( "world_size_slider", label="World Scale", min=0, max=100, fieldMaxValue=200, field=True, value=1 )
        cmds.separator( height=25, style="none" )

        cmds.text( label="Delete the history after deforming the object." )
        cmds.separator( height=5, style="none" )
        self.button_delete_history = cmds.button( label="Delete Construction History", width=150, command=self.delete_history_button )

        
    # Duplicates the currently selected object(s) and combines them.  We don't want to override the original.
    # The pivot is moved to the bottom center of the new object.
    # It's then placed at the origin where the transformations are frozen and the history is deleted.
    def duplicate_button( self, *args  ):
        self.original_selected_objects = cmds.ls( selection=True )

        if( len(self.original_selected_objects) == 0 ):
            print "Nothing selected"
            return 0

        elif( len(self.original_selected_objects) == 1 ):
            self.relatives = cmds.listRelatives( children=True )

            if( len(self.relatives) == 1 ):
                print "Skip combine"
                cmds.duplicate( self.original_selected_objects, name=self.original_selected_objects[0] + "_Copy" )
                cmds.delete( constructionHistory=True )
                the_parent = cmds.listRelatives( parent=True )
                if( the_parent != None ):
                    cmds.parent( self.original_selected_objects[0] + "_Copy", world=True )

            else:
                self.combine()

        else:
            self.combine()

        self.newOriginCopy = cmds.ls( selection=True )[0]
        self.bbox = cmds.exactWorldBoundingBox( self.newOriginCopy )
        cmds.move((self.bbox[0] + self.bbox[3])/2, self.bbox[1], (self.bbox[2] + self.bbox[5])/2, self.newOriginCopy + ".scalePivot", self.newOriginCopy + ".rotatePivot", absolute=True)
        cmds.move( 0, 0, 0, self.newOriginCopy, rpr=True )
        cmds.makeIdentity( apply=True, t=1, r=1, s=1 )
        cmds.delete( constructionHistory=True )


    # Creates two non-linear bend deformers at the base of the object to bulge it up from the bottom.
    def bulge_button( self, *args  ):
        if( cmds.objExists( "ZBend" ) ):
            cmds.confirmDialog( title="Error", message="First delete the bulge history on the previously\ndeformed object before bulging another.", button="Okie Dokie" )
            return 0

        latestSelection = cmds.ls( selection=True )
        if( len( latestSelection ) == 0 ):
            return 0

        if( len( latestSelection ) == 1 ):
            self.relatives = cmds.listRelatives( children=True )

            if( len(self.relatives) == 1 ):
                self.bbox = cmds.exactWorldBoundingBox( latestSelection )

                cmds.nonLinear( type='bend', curvature=cmds.intSliderGrp( "x_bulge_slider", value=True, query=True ) )
                cmds.rename( "XBend" )
                cmds.move((self.bbox[0] + self.bbox[3])/2, self.bbox[1], (self.bbox[2] + self.bbox[5])/2, "XBend", rpr=True )
                cmds.setAttr( "XBend.rotateZ", -90 )

                cmds.select( latestSelection )

                cmds.nonLinear( type='bend', curvature=cmds.intSliderGrp( "z_bulge_slider", value=True, query=True ) )
                cmds.rename( "ZBend" )
                cmds.move((self.bbox[0] + self.bbox[3])/2, self.bbox[1], (self.bbox[2] + self.bbox[5])/2, "ZBend", rpr=True )
                cmds.setAttr( "ZBend.rotateZ", -90 )
                cmds.setAttr( "ZBend.rotateX", 90 )
                cmds.connectControl( "x_bulge_slider", "bend1.curvature" )
                cmds.connectControl( "z_bulge_slider", "bend2.curvature" )
                cmds.select( latestSelection )

    # Builds a sphere in proportion to our round world so we can see if the bulging is the correct amount.
    def create_world_button( self, *args  ):
        if( cmds.objExists( "OurSampleWorld" ) ):
            return 0
        else:
            cmds.sphere( r=10, sections=40, spans=30, name="OurSampleWorld" )
            cmds.setAttr( "OurSampleWorld.scale", 9.599, 9.599, 9.599 )
            cmds.makeIdentity( apply=True, t=1, r=1, s=1 )
            self.wbbox = cmds.exactWorldBoundingBox( "OurSampleWorld" )
            cmds.move((self.wbbox[0] + self.wbbox[3])/2, self.wbbox[4], (self.wbbox[2] + self.wbbox[5])/2, "OurSampleWorld.scalePivot", "OurSampleWorld.rotatePivot", absolute=True)
            cmds.move( 0, 0, 0, "OurSampleWorld", rpr=True )
            cmds.connectControl( "world_size_slider", "OurSampleWorld.scaleX", "OurSampleWorld.scaleY", "OurSampleWorld.scaleZ" )
        
    # Option to wipe any selected object's history.
    def delete_history_button( self, *args  ):
        selection = cmds.ls( selection=True )

        if( len(selection) == 0 ):
            print "Nothing selected"
        else:
            cmds.delete( constructionHistory=True )

    # Function to combine all the selected geometry into one piece for bulging and exporting.
    def combine( self ):
        cmds.duplicate( self.original_selected_objects, name="special_copy" )
        self.selected_objects = cmds.ls( selection=True )
        self.duplicate_name = self.original_selected_objects[0] + "_Combined_Copy"
        cmds.polyUnite( self.selected_objects, name=self.duplicate_name )
        cmds.delete( constructionHistory=True )
        if( len(cmds.ls( "special_copy" )) == 1 ):
            cmds.delete( self.selected_objects )


    # The Close button destroys the bulge creator window
    def close_button( self, *args ):
        self.destroy()
        
our_bulge_window = Bulge_Window()
our_bulge_window.create()
