from flet import *
import sqlite3

conn = sqlite3.connect("dato.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS student(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stdname TEXT,
    stdmail TEXT,
    stdphone TEXT,
    stdaddress TEXT,
    stmathmatic INTEGER ,
    starabic INTEGER,
    stfrance INTEGER,
    stenglish INTEGER,
    stdrawing INTEGER,
    stchemistry INTEGER
)""")
conn.commit()


def main(page: Page):
    page.title = 'نظام إدارة الطلاب'
    page.scroll = 'auto'  # شريط تمرير تلقائي
    page.window.top = 1
    page.window.left = 960
    page.window.width = 390
    page.window.height = 740
    page.bgcolor = '#F0F0F0'
    page.theme_mode = ThemeMode.LIGHT
    page.rtl = True

    # تحديث عدد الطلاب
    def update_count():
        cursor.execute('SELECT COUNT(*) FROM student')
        return cursor.fetchone()[0]

    # إضافة طالب جديد
    def add(e):
        # التحقق من الحقول
        if not tname.value or not tmail.value or not tphone.value or not taddress.value:
            page.snack_bar = SnackBar(Text("❌ الرجاء ملء جميع الحقول!", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        try:
            cursor.execute("""INSERT INTO student 
                (stdname, stdmail, stdphone, stdaddress, stmathmatic, starabic, stfrance, stenglish, stdrawing, stchemistry) 
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                           (tname.value, tmail.value, tphone.value, taddress.value,
                            int(mathmatic.value) if mathmatic.value else 0,
                            int(arabic.value) if arabic.value else 0,
                            int(france.value) if france.value else 0,
                            int(english.value) if english.value else 0,
                            int(draw.value) if draw.value else 0,
                            int(chemistry.value) if chemistry.value else 0))
            conn.commit()

            # مسح الحقول
            tname.value = ""
            tmail.value = ""
            tphone.value = ""
            taddress.value = ""
            mathmatic.value = ""
            arabic.value = ""
            france.value = ""
            english.value = ""
            draw.value = ""
            chemistry.value = ""

            # تحديث العدد
            count_text.value = str(update_count())
            page.snack_bar = SnackBar(Text("✅ تم إضافة الطالب بنجاح!", color="white"), bgcolor="green")
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            print(f"خطأ: {ex}")

    # عرض كل الطلاب
    def show(e):
        # تنظيف الصفحة وعرض شريط العنوان مع زر الرجوع
        page.clean()

        # إضافة AppBar مع زر الرجوع
        page.appbar = AppBar(
            title=Text("📋 قائمة الطلاب", size=20, weight='bold'),
            center_title=False,
            bgcolor='#2196F3',
            leading=TextButton(
                "رجوع",
                style=ButtonStyle(color='white'),
                on_click=go_back
            ),
            actions=[
                TextButton(
                    "تحديث",
                    style=ButtonStyle(color='white'),
                    on_click=show
                )
            ]
        )

        cursor.execute("SELECT * FROM student")
        users = cursor.fetchall()

        if not users:
            page.add(
                Column([
                    Container(
                        content=Text("📭", size=80),
                    ),
                    Container(
                        content=Text("لا يوجد طلاب مسجلين", size=20, color="gray"),
                    ),
                ], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=20)
            )
            page.update()
            return

        # استخدام ListView للتمرير في حالة البيانات المتعددة
        students_list = ListView(expand=True, spacing=10, padding=10)

        for user in users:
            # حساب المجموع
            total = sum(user[5:11])
            status = "✅ ناجح" if total >= 50 else "❌ راسب"
            status_color = "#4CAF50" if total >= 50 else "#f44336"

            students_list.controls.append(
                Card(
                    elevation=3,
                    content=Container(
                        padding=15,
                        content=Column([
                            # الاسم والبريد
                            Container(
                                content=Row([
                                    Text("👨‍🎓", size=28),
                                    Column([
                                        Text(user[1], size=18, weight='bold'),
                                        Text(user[2], size=12, color='gray'),
                                    ], spacing=2)
                                ]),
                                padding=5
                            ),

                            Divider(),

                            # معلومات الاتصال
                            Row([
                                Text("📱", size=14),
                                Text(user[3], size=14),
                                Text("📍", size=14),
                                Text(user[4], size=14),
                            ], spacing=10),

                            Divider(),

                            # العلامات
                            Text("📊 العلامات", weight='bold', size=14),
                            Row([
                                Column([
                                    Text("📐", size=12),
                                    Text(str(user[5]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                                Column([
                                    Text("📖", size=12),
                                    Text(str(user[6]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                                Column([
                                    Text("🥖", size=12),
                                    Text(str(user[7]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                                Column([
                                    Text("🇬🇧", size=12),
                                    Text(str(user[8]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                                Column([
                                    Text("🎨", size=12),
                                    Text(str(user[9]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                                Column([
                                    Text("🧪", size=12),
                                    Text(str(user[10]), size=16, weight='bold', color='blue')
                                ], horizontal_alignment=CrossAxisAlignment.CENTER),
                            ], alignment=MainAxisAlignment.SPACE_AROUND),

                            Divider(),

                            # النتيجة
                            Container(
                                content=Row([
                                    Text("🎯 المجموع:", weight='bold'),
                                    Text(str(total), size=16, weight='bold', color='orange'),
                                    Container(
                                        content=Text(status, color='white', size=14),
                                        bgcolor=status_color,
                                        padding=5,
                                        border_radius=10
                                    )
                                ], alignment=MainAxisAlignment.SPACE_AROUND),
                                padding=5
                            )
                        ], spacing=10)
                    )
                )
            )

        page.add(students_list)
        page.update()

    # العودة للرئيسية
    def go_back(e):
        page.clean()
        page.appbar = None  # إزالة شريط العنوان
        build_main()
        page.update()

    # بناء الواجهة الرئيسية
    def build_main():
        current_count = update_count()
        count_text.value = str(current_count)

        # إضافة AppBar للصفحة الرئيسية
        page.appbar = AppBar(
            title=Text("🏠 الرئيسية", size=20, weight='bold'),
            center_title=False,
            bgcolor='#2196F3',
        )

        # استخدام Column مع scroll للتمرير
        main_content = Column(
            scroll='auto',  # شريط تمرير
            spacing=10,
            controls=[
                # الشعار
                Container(
                    content=Text("📚", size=70),
                    margin=Margin.only(top=20)
                ),

                Container(
                    content=Text("نظام إدارة الطلاب", size=24, weight='bold', color='#2196F3'),
                    margin=Margin.only(bottom=5)
                ),

                Container(
                    content=Text("تطبيق الطالب والمعلم في جيبك", size=14, color='gray'),
                    margin=Margin.only(bottom=20)
                ),

                # عدد الطلاب
                Container(
                    content=Row([
                        Text("👥", size=20),
                        Text("عدد الطلاب المسجلين:", size=16, weight='bold'),
                        count_text
                    ], alignment=MainAxisAlignment.CENTER),
                    bgcolor='#E3F2FD',
                    padding=10,
                    border_radius=10,
                    margin=Margin.only(bottom=20)
                ),

                # حقول الإدخال
                Container(
                    content=Column([
                        Text("📝 معلومات الطالب", size=16, weight='bold', color='#2196F3'),
                        tname, tmail, tphone, taddress,

                        Divider(),

                        Text("📊 العلامات الدراسية", size=16, weight='bold', color='#2196F3'),
                        Row([mathmatic, arabic, france], alignment=MainAxisAlignment.CENTER),
                        Row([english, draw, chemistry], alignment=MainAxisAlignment.CENTER),
                    ], spacing=10),
                    padding=10
                ),

                # الأزرار
                Container(
                    content=Row([
                        add_button,
                        show_button
                    ], alignment=MainAxisAlignment.CENTER, spacing=20),
                    margin=Margin.only(top=20, bottom=20)
                )
            ]
        )

        page.add(main_content)

    # تحديث الصفحة الرئيسية
    def refresh_main(e):
        page.clean()
        build_main()
        page.update()

    # إنشاء الحقول
    tname = TextField(label='✏️ اسم الطالب', rtl=True, height=40)
    tmail = TextField(label='📧 البريد الالكتروني', rtl=True, height=40)
    tphone = TextField(label='📞 رقم الهاتف', rtl=True, height=40)
    taddress = TextField(label='🏠 العنوان', rtl=True, height=40)

    mathmatic = TextField(label='📐 رياضيات', width=100, text_align=TextAlign.CENTER, height=40)
    arabic = TextField(label='📖 عربي', width=100, text_align=TextAlign.CENTER, height=40)
    france = TextField(label='🥖 فرنسية', width=100, text_align=TextAlign.CENTER, height=40)
    english = TextField(label='🇬🇧 انجليزية', width=100, text_align=TextAlign.CENTER, height=40)
    draw = TextField(label='🎨 رسم', width=100, text_align=TextAlign.CENTER, height=40)
    chemistry = TextField(label='🧪 كيمياء', width=100, text_align=TextAlign.CENTER, height=40)

    add_button = Button(
        "➕ إضافة طالب جديد",
        width=170,
        style=ButtonStyle(bgcolor='#4CAF50', color='white'),
        on_click=add
    )

    show_button = Button(
        "👁️ عرض كل الطلاب",
        width=170,
        style=ButtonStyle(bgcolor='#2196F3', color='white'),
        on_click=show
    )

    count_text = Text(str(update_count()), size=18, weight='bold', color='#2196F3')

    # بناء الواجهة
    build_main()
    page.update()


# تشغيل التطبيق
run(main)
