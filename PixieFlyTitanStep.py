import bpy

# アドオン情報（名前やバージョンなど）
bl_info = {
    "name": "Pixie Fly Titan Step",
    "author": "Pon Pon Games",
    "version": (0, 1),
    "blender": (3, 4, 0),
    "location": "3D Viewport > Pose > Select All Location Keys",
    "description": "Scale all Location Keys of current action.",
    "warning": "Not enough debugging. This addon can cause crashes.",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Animation"
}

# Log
# 0: Warn and Error
# 1: Debug
# 2: Debug (Noisy)
def print_log(text, level):
    level_max = 0
    if level <= level_max:
        print(text)

# Blender起動後の初回のアドオン有効時だけ呼ばれます。
print_log("Pixie Fly Titan Step is called", 1)

# 制御オペレータ
# 状態をトグルします。UIに追加したボタンから呼ばれます。
class PixieFlyTitanStep_OT_ScaleKeyLocs(bpy.types.Operator):
    bl_idname = "onesteptolocal.scalekeylocs"
    bl_label = "Scale All Location Keys"
    bl_description = "Scale all Location Keys of current action."
    bl_options = {'REGISTER', 'UNDO'}

    scale_val: bpy.props.FloatProperty(
        name="Scale",
        description="Scale value for Location Keys.",
        default=1.0,
    )

    @classmethod
    def poll(cls, context):
        return "fcurves" in dir(context.active_object.animation_data.action)

    def execute(self, context):
        print_log("F-Curve Loc Scaling Begins.", 1)
        for fc in bpy.context.active_object.animation_data.action.fcurves:
            if fc.data_path.find(".location") >= 0:
                print("data_path = ", fc.data_path)
                for point in fc.keyframe_points:
                    oldVal = point.co[1]
                    newVal = oldVal * self.scale_val
                    point.co[1] = newVal
                fc.update()
        print_log("F-Curve Loc Scaling Ends", 1)
        return {'FINISHED'}

def add_menu_item(self, context):
    self.layout.separator()
    self.layout.operator(PixieFlyTitanStep_OT_ScaleKeyLocs.bl_idname)

# アドオンを有効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def register():
    print_log("register is called.", 1)
    bpy.utils.register_class(PixieFlyTitanStep_OT_ScaleKeyLocs)
    bpy.types.VIEW3D_MT_pose.append(add_menu_item)

# アドオンを無効にしたときにBlenderから呼ばれます。
# このとき、bpy.dataとbpy.contextにアクセス不可。
def unregister():
    print_log("unregister is called", 1)
    bpy.types.VIEW3D_MT_pose.remove(add_menu_item)
    bpy.utils.unregister_class(PixieFlyTitanStep_OT_ScaleKeyLocs)

# Blenderのテキストエディタで呼んだときの処理（デバッグ用）
if __name__ == "__main__":
    print_log("Pixie Fly Titan Step is called from main", 1)
    register()
    #unregister()

