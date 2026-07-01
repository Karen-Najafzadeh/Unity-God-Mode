# الگوی ساختاری Object Pooling (مکانیک‌های پایین‌سطح سخت‌افزار)

#### 1. مقدمه و زمینه معماری

در بررسی قبلی خود از Garbage Collector افزایشی، دیدیم که موتورهای مدرن وظایف پاک‌سازی را بین چند بخش تقسیم می‌کنند تا از یخ‌زدگی‌های میکرو جلوگیری کنند. با این حال، تکیه بر این رویکرد برای تنظیم سرعت کار janitor هنوز یک استراتژی واکنشی است. بالاترین سطح معماری عملکرد در بازی، رویکردی رادیکال‌تر را می‌طلبد: دیگر زباله تولید نکنید.

در اینجا الگوی ساختاری Object Pooling وارد می‌شود. به جای اینکه بارها و بارها ظرف‌های داده را بسازید، تخریب کنید و رها کنید (GameObjectها، ساختارهای داده یا آرایه‌ها)، Object Pooling یک نیروی کار دائمی و ثابت را از همان ابتدای اجرای برنامه آماده نگه می‌دارد.

فکر کنید مثل یک کتابخانه یا کشوی ابزارهای اجاره‌ای ویژه است. وقتی بازیکن یک سلاح خودکار شلیک می‌کند، موتور یک پرتابه را از هیچ‌جا خلق نمی‌کند، آن را برای ۰.۸ ثانیه در اتاق پرواز می‌دهد و سپس اجازه نمی‌دهد که به زباله مرده تبدیل شود. در عوض، یک گلوله خواب‌آلود و از پیش ساخته‌شده را از یک کابینت منظم بیرون می‌آورد، موقعیت فیزیکی آن را به لبه لوله تفنگ منتقل می‌کند، آن را بیدار می‌کند و به سمت هدف می‌فرستد. لحظه‌ای که آن گلوله به دیوار بتنی برخورد می‌کند، از بین نمی‌رود؛ در عوض، معیارهای خود را بازنشانی می‌کند، بینایی و شنوایی‌اش را خاموش می‌کند و آرام آرام دوباره به کشوی ذخیره برمی‌گردد تا برای شلیک بعدی آماده بماند.

---

#### 2. روایت علوم رایانه: هزینه ساخت و تخریب

برای درک این‌که چرا این الگو در طراحی موتور بازی بسیار مقدس است، باید به lore تاریخی تاریک مدیریت حافظه در دوران اولیه نگاه کنیم. در سیستم‌های نرم‌افزاری اولیه، توسعه‌دهندگان به شدت به مکانیزم‌های خام new و delete وابسته بودند. برای انسانِ نوشته‌کننده کد، تایپ کردن Instantiate(projectilePrefab) شبیه یک اعلان ساده و یک‌مرحله‌ای به نظر می‌رسد. اما برای سیلیکون فیزیکی رایانه، این یک فاجعه چندبخشِ اداری است.

وقتی از موتور می‌خواهید یک موجودیت تازه را در میانه یک فریم ایجاد کند، این توالی در ماشین فعال می‌شود:

1. جست‌وجوی انبار: زمان اجرا کار فعلی را متوقف می‌کند و از میان Heap (انبار حافظه) برای یافتن یک بلوک متوالی از فضای خالی که اندازه کافی برای شیء جدید داشته باشد، جست‌وجو می‌کند.
2. رژه سازنده‌ها: پس از تأمین فضای لازم، سیستم‌عامل سازنده‌های شیء را اجرا می‌کند؛ تنظیم هم‌ترازی حافظه، ثبت مؤلفه‌ها و ارزیابی وابستگی‌های سیستمی.
3. ثبت هسته موتور: Unity باید این شیء جدید را به ماتریس‌های ردیابی خود وصل کند، از جمله Physics Engine (PhysX/Havok) برای ردیابی برخورد، Transform Hierarchy برای والدین موقعیتی و Render Pipeline برای قابلیت مشاهده در دوربین.
4. شهر ارواح باقی‌مانده: هنگامی که موجودیت از طریق Destroy() از بین می‌رود، موتور همه این پیوندهای ساختاری را قطع می‌کند. آدرس حافظه رها می‌شود و یک شکاف فیزیکی در کف انبار باقی می‌ماند.

در دوران اولیه بازی‌های سه‌بعدی، توسعه‌دهندگانی که این هزینه را نادیده می‌گرفتند، متوجه می‌شدند که بازی در هنگام قدم زدن در راهرو خالی با ۹۰ فریم بر ثانیه اجرا می‌شود، اما در لحظه شروع درگیری شدید به ۱۵ فریم بر ثانیه سقوط می‌کند. سخت‌افزار برای کشیدن گلوله‌ها مشکل نداشت؛ بلکه در برابر کارهای اداری spawning و killing خفه می‌شد. Object Pooling برای تبدیل بازی از حالت بازسازی مداوم و ناپایدار در زمان اجرا به حالت ثبات معماری دائمی ابداع شد.

---

#### 3. مسئله اصلی: Heap «پنیر سوئیسی» و پل‌های داخلی موتور

حتی اگر یک توسعه‌دهنده بازی از Incremental Garbage Collector استفاده کند، ورود زیاد تخصیص‌های زمان اجرا دو اثر مخرب ایجاد می‌کند که می‌تواند خط پایه عملکرد موتور بازی را خراب کند:

##### A. Fragmentation حافظه («چیدمان پنیر سوئیسی»)

اگر بازی شما به‌طور مداوم اشیاء با اندازه‌های بایت مختلف را نمونه‌سازی و نابود می‌کند (مثلاً یک پرتابه ۶۴ بایتی، یک افکت ذره دشمن ۲۵۶ بایتی و یک توکن صوتی ۸۰ بایتی)، انبار حافظه شما بسیار fragmented می‌شود.

تصور کنید یک پارکینگ دارید که در آن خودروها به‌طور تصادفی می‌آیند و می‌روند. بعد از چند ساعت، شاید ۵۰ فضای خالی داشته باشید، اما همه آن‌ها جای‌های جداگانه و پراکنده‌اند. اگر یک اتوبوس بزرگ (یک آرایه بزرگ یا یک ساختار داده پیچیده) برسد، آنجا نمی‌تواند پارک کند، چون یک بلوک پیوسته و کافی از فضای خالی وجود ندارد، حتی اگر حجم کل فضای آزاد از نظر تئوری کافی باشد. این موضوع مجبور می‌کند سیستم یک Routine فشرده‌سازی حافظه اضطراری اجرا کند یا با خطای Out of Memory مواجه شود.

##### B. churn bridge C++ به C#

Unity یک موتور هیبریدی است. محیط بالای سطح گیم‌پلی آن در یک زمان‌اجرا C# مدیریت‌شده اجرا می‌شود، اما موتورهای زیرین با عملکرد بالا برای رندر، فیزیک و مدیریت منابع در C++ خام و unmanaged نوشته شده‌اند.

هر بار که MonoBehaviour.Instantiate یا MonoBehaviour.Destroy را فراخوانی می‌کنید، موتور مجبور می‌شود یک پل ارتباطی پرهزینه بین این دو مرز بسازد. این پل interop نیازمند Marshalling (ترجمه قالب داده‌ها بین چیدمان C# و چیدمان حافظه C++)، جست‌وجوی اشاره‌گر و ثبت‌نام‌های مختلف است. انجام این کار ده‌ها بار در هر فریم، یک مانع عملکردی اصلی ایجاد می‌کند و میلیون‌ها چرخه CPU را صرف ترجمه داده‌ها می‌کند.

---

#### 4. چگونه این مشکل را حل می‌کند: راز چیزی که «خدایان یونیتی» نادیده گرفته‌اند

بیشتر توسعه‌دهندگان میانی می‌دانند که Object Pooling هزینه تخصیص را کاهش می‌دهد. اما بیایید یک مکانیزم عمیق‌تر را بررسی کنیم که در مستندات استاندارد به آن اشاره نمی‌شود: Locality خط cache L1/L2 CPU و بهینه‌سازی Prefetching سخت‌افزار.

پردازنده‌های مدرن رایانه داده‌ها را از RAM اصلی یک بایت در یک بایت نمی‌خوانند. RAM از نظر فیزیکی خیلی دور از CPU قرار دارد و بنابراین بسیار کند است. در عوض، CPU مجموعه‌ای از حافظه‌های بسیار سریع درون خود به نام L1، L2 و L3 Cache دارد. وقتی CPU داده‌ای را از یک آدرس خاص درخواست می‌کند، یک کل Cache Line (معمولاً ۶۴ بایت پیوسته) را به L1 cache محلی خود می‌کشاند، با فرض این‌که داده‌های کنار آن هم در آینده نیاز خواهند شد. این پدیده Spatial Locality نام دارد.

- مشکل Instantiation کلاسیک: وقتی Instantiate() را فراخوانی می‌کنید، انبار هر جای خالی را که بتواند پیدا کند اختصاص می‌دهد. این کار گلوله‌های شما را در آدرس‌های کاملاً تصادفی و جدا از هم در RAM پخش می‌کند. وقتی بازی از طریق یک لیست گلوله‌های فعال برای حرکت آن‌ها عبور می‌کند، CPU مجبور می‌شود از یک آدرس دوردست به آدرس دیگری جهش کند. این موضوع تقریباً برای هر گلوله باعث Cache Miss می‌شود و پردازنده را وادار می‌کند برای صدها چرخه CPU بی‌کار بماند تا داده‌ها از RAM کند منتقل شوند.
- معماری Pooling حاکم: وقتی یک Object Pool را به صورت آرایه‌ای پیوسته و فشرده یا ساختاری ترتیبی در ابتدای اجرا پیش‌تخصیص می‌دهید، سیستم‌عامل این اشیاء را در کنار هم در سیلیکون فیزیکی قرار می‌دهد. وقتی CPU Bullet 1 را پردازش می‌کند، Prefetcher سخت‌افزار به‌طور خودکار داده‌های Bullet 2، Bullet 3 و Bullet 4 را پیش از نیاز به خطوط cache L1/L2 منتقل می‌کند. عملیات حلقه با سرعت فوق‌العاده اجرا می‌شوند، چون پردازنده همه داده‌های لازم را در همان میز کار خود پیدا می‌کند و یک ماشین حافظه‌ای کند و لرزان را به یک دستگاه جریان‌محور با عملکرد بالا تبدیل می‌کند.

---

#### 5. مثال‌های کدنویسی

بیایید تفاوت معماری بین یک طراحی پر-تخصیص و یک سیستم پیشرفته Object Pooling بدون تخصیص و بهینه‌شده برای cache را بررسی کنیم.

---

##### 1. ❌ معماری تخصیص‌محور ساده (عامل کاهش عملکرد)

این اسکریپت یک الگوی رایج در بسیاری از بازی‌ها را نشان می‌دهد: یک افکت flash muzzle و یک پرتابه را در یک تایمر تکراری ایجاد می‌کند و سپس به کمک زمان‌بندهای تخریب استاندارد آن‌ها را پاک می‌کند.

```csharp
using UnityEngine;

public class NaiveWeaponSystem : MonoBehaviour
{
    public GameObject projectilePrefab;
    public GameObject muzzleFlashPrefab;
    public Transform firePoint;

    void Update()
    {
        if (Input.GetKey(KeyCode.Space))
        {
            // ❌ FAILURE MECHANICAL: یک GameObject جدید را در Heap می‌سازد.
            // هزینه bridge C++ به C# و fragmentation حافظه را ایجاد می‌کند.
            GameObject bullet = Instantiate(projectilePrefab, firePoint.position, firePoint.rotation);
            
            // ❌ FAILURE MECHANICAL: یک موجودیت کوتاه‌مدت تصویری دیگر هم ایجاد می‌کند.
            GameObject flash = Instantiate(muzzleFlashPrefab, firePoint.position, firePoint.rotation);

            // ❌ FAILURE MECHANICAL: یک Routine پرهزینه ردیابی موتور را مجبور می‌کند.
            // اشیاء را برای تخریب در Heap زمان‌بندی می‌کند و تضمین می‌کند که در آینده GC sweeps رخ دهد.
            Destroy(bullet, 2.0f);
            Destroy(flash, 0.2f);
        }
    }
}
```

---

##### 2. معماری ساده و سفارشی Object Pool (الگوی پایه)

برای درک این‌که یک سیستم پیشرفته در پشت صحنه چگونه کار می‌کند، باید ابتدا یک Object Pool سفارشی ساده را ببینیم. این کار را با استفاده از ساختار Queue استاندارد C# می‌سازیم. Queue را می‌توان مانند صف واقعی اشیاء در صندوق فروشگاه تصور کرد: اولین شیء واردشده، اولین شیء خارج‌شده است (FIFO: First-In, First-Out).

##### 🛠️ پیاده‌سازی ساده Pool سفارشی

```csharp
using System.Collections.Generic;
using UnityEngine;

public class SimpleCustomObjectPool : MonoBehaviour
{
    [Header("Pool Setup")]
    [SerializeField] private GameObject bulletPrefab;
    [SerializeField] private int initialPoolSize = 20;

    // 📦 کابینت: یک Queue ساده برای نگهداری اشیاء خواب‌آلود در حافظه
    private Queue<GameObject> poolStorage = new Queue<GameObject>();

    void Start()
    {
        // پیش‌تخصیص اشیاء درست در زمان راه‌اندازی، قبل از آن‌که بازیکن حتی بتواند شلیک کند
        for (int i = 0; i < initialPoolSize; i++)
        {
            GameObject obj = Instantiate(bulletPrefab);
            
            // بلافاصله آن را به خواب ببرید تا در فضا شناور نباشد یا منطق آن اجرا شود
            obj.SetActive(false);
            
            // آن را در Queue کابینت ذخیره کنید
            poolStorage.Enqueue(obj);
        }
    }

    /// <summary>
    /// دفتر استخراج: یک گلوله را از صف ذخیره‌مان بیرون می‌آورد.
    /// </summary>
    public GameObject GetBullet()
    {
        // بررسی ایمنی: اگر بازیکن سریع‌تر از آن‌چه Pool می‌تواند مدیریت کند شلیک کند چه؟
        // اگر کابینت خالی باشد، مجبوریم یک شیء پشتیبان اضطراری را به‌صورت پویا بسازیم.
        if (poolStorage.Count == 0)
        {
            Debug.LogWarning("Pool ran completely dry! Dynamically allocating an emergency backup object.");
            GameObject emergencyObj = Instantiate(bulletPrefab);
            return emergencyObj;
        }

        // قدیمی‌ترین شیء استراحت‌کرده را از صف بیرون بکشید
        GameObject activeObj = poolStorage.Dequeue();
        
        // آن را بیدار کنید! آن را دوباره به جهان بازی برگردانید
        activeObj.SetActive(true);
        
        return activeObj;
    }

    /// <summary>
    /// میز بازگشت: یک گلوله قدیمی را دوباره به کابینت برمی‌گرداند، نه اینکه آن را نابود کند.
    /// </summary>
    public void ReturnBullet(GameObject obj)
    {
        // شیء را کور و خفته کنید تا رندر و فیزیک محاسبه نشوند
        obj.SetActive(false);

        // آن را ایمن دوباره به صف ذخیره‌مان فشار دهید
        poolStorage.Enqueue(obj);
    }
}
```

---

این نمونه نشان می‌دهد که چگونه بعد از ساخت Pool از آن استفاده می‌شود.

```csharp
using UnityEngine;

public class Gun : MonoBehaviour
{
    // مرجع به Pool سفارشی ما.
    // این را در Inspector مقدار‌دهی کنید. (هنوز از Singleton استفاده نمی‌کنیم)
    [SerializeField] private SimpleCustomObjectPool bulletPool;

    // نقطه‌ای که گلوله‌ها باید از آنجا ظاهر شوند.
    [SerializeField] private Transform firePoint;

    void Update()
    {
        // هر زمان دکمه چپ ماوس فشرده شود، گلوله‌ای شلیک شود.
        if (Input.GetMouseButtonDown(0))
        {
            Fire();
        }
    }

    private void Fire()
    {
        // از Pool یک گلوله در دسترس بخواهید.
        // در اینجا Instantiate() اتفاق نمی‌افتد مگر اینکه Pool خالی باشد.
        GameObject bullet = bulletPool.GetBullet();

        // گلوله بازیافتی را به دهانه سلاح منتقل کنید.
        bullet.transform.position = firePoint.position;

        // جهت گلوله را با جهت سلاح یکسان کنید.
        bullet.transform.rotation = firePoint.rotation;

        // به آن سرعت رو به جلو بدهید.
        // (فرض بر این است که گلوله دارای Rigidbody است.)
        Rigidbody rb = bullet.GetComponent<Rigidbody>();

        if (rb != null)
        {
            // هرگونه حرکت باقیمانده از زندگی قبلی را پاک کنید.
            rb.linearVelocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;

            // گلوله را به جلو شلیک کنید.
            rb.linearVelocity = firePoint.forward * 20f;
        }

        // چون این Pool ساده به‌طور خودکار گلوله‌ها را بازپس نمی‌گیرد،
        // این گلوله را بعد از ۳ ثانیه برمی‌گردانیم.
        Invoke(nameof(ReturnBullet), 3f);

        // مرجع گلوله را ذخیره می‌کنیم تا Invoke() بداند کدام را بازگرداند.
        bulletToReturn = bullet;
    }

    // آخرین گلوله شلیک‌شده را نگه می‌دارد.
    // (این فقط برای ساده نگه داشتن مثال است.)
    private GameObject bulletToReturn;

    private void ReturnBullet()
    {
        // گلوله را به Pool برگردانید، نه اینکه آن را نابود کنید.
        bulletPool.ReturnBullet(bulletToReturn);
    }
}
```

##### ⚠️ محدودیت‌های معماری ساده

اگرچه این Pool سفارشی مفهوم اصلی را بسیار خوب نشان می‌دهد، دارای نقایص معماری مهمی است که آن را برای توسعه بازی‌های در مقیاس بزرگ و enterprise نامناسب می‌کند:

- فروپاشی کابینت خالی: اگر Pool تمام شود، بدون سقف ایمنی به‌صورت بی‌نهایت با تخصیص پویا رشد می‌کند و در معرض خطر Crash حافظه قرار می‌گیرد.
- نبود چک‌های ایمنی داخلی: اگر توسعه‌دهنده به اشتباه همان گلوله را دوبار به Pool بازگرداند، شیء دوبار در Queue وجود خواهد داشت. این کار منطق صف را از بین می‌برد و باعث باگ‌های عجیب می‌شود که یک گلوله فعال ناگهان دیگر را کنترل یا جابه‌جا می‌کند.
- نبود Alignment مناسب برای cache: Queue خام C# تضمین نمی‌کند که چیدمان فضایی بهینه‌ای در خطوط cache CPU داشته باشد و این فرصت بهبودهای جزئی عملکرد را باقی می‌گذارد.

> توجه: این مثال به‌طور عمدی حداقلی و آموزشی است. اسکریپت مصرف‌کننده (Gun) محدودیت‌هایی دارد؛ برای مثال، اگر چند گلوله را در عرض ۳ ثانیه شلیک کنید، bulletToReturn بازنویسی می‌شود و فقط آخرین گلوله درست بازگردانده می‌شود.

> برای یک بازی واقعی، معمولاً هر گلوله خودش بازمی‌گردد (یا یک coroutine جداگانه برای هر گلوله مدیریت می‌کند)، اما برای نشان دادن «این‌طور از Pool استفاده می‌شود»، این نسخه ساده نگه داشته شده است.

---

##### 3. معماری پیشرفته و حاکم Object Pool (سیستم مدرن Unity)

برای دور زدن این محدودیت‌ها کاملاً، نسخه‌های مدرن Unity یک معماری پیشرفته و بهینه‌شده native pooling را در فضای نام UnityEngine.Pool ارائه می‌دهند.

این فریم‌ورک enterprise جایگزین آرایه‌ها یا لیست‌های دستی می‌شود و زیرساختی بسیار قوی فراهم می‌کند که شامل ردیابی تکراری، مرزهای مقیاس‌پذیری، بهینه‌سازی حافظه پیش‌تخصیص‌شده و شیرهای ایمنی برای نابودسازی اشیاء در صورت overflow است.

##### 👑 پیاده‌سازی کد تولیدی و پیشرفته

در زیر یک چارچوب معماری تولیدی کامل آمده است. این کار به دو اسکریپت مجزا تقسیم شده است: کنترل‌کننده اصلی سلاح که انبار حافظه را مدیریت می‌کند و یک اسکریپت همراه متصل به پرتابه برای خودکارسازی چرخه عمر آن.

```csharp
using UnityEngine;
using UnityEngine.Pool; // 👑 از فریم‌ورک native و بسیار بهینه Unity Pool استفاده می‌کند

public class SovereignWeaponSystem : MonoBehaviour
{
    [Header("Pool Configurations")]
    [SerializeField] private GameObject projectilePrefab;
    [SerializeField] private int defaultPoolCapacity = 50;
    [SerializeField] private int maxPoolSafetyCeiling = 100;

    [Header("Weapon Anchors")]
    [SerializeField] private Transform firePoint;

    // 👑 قلب معماری: یک interface ساختاری با نوع قوی برای Pool.
    // این جایگزین Queue‌های ساده می‌شود و از یک framework داخلی با ردیابی عمیق سخت‌افزاری استفاده می‌کند.
    private IObjectPool<GameObject> projectilePool;

    void Awake()
    {
        // blueprint عملیاتی روشن Pool را در زمان راه‌اندازی پیکربندی کنید.
        // چهار callback حیاتی را ارائه می‌دهیم که نحوه مدیریت حافظه را تعیین می‌کنند.
        projectilePool = new ObjectPool<GameObject>(
            createFunc: OnCreatePooledItem,          // قانون 1: چگونه یک شیء جدید اگر Pool تمام شود بسازیم
            actionOnGet: OnTakeItemFromPool,         // قانون 2: چگونه یک شیء را بیدار و برای ورود به جهان آماده کنیم
            actionOnRelease: OnReturnItemToPool,     // قانون 3: چگونه یک شیء را کور و خواب‌آلود در کابینت قرار دهیم
            actionOnDestroy: OnDestroyPooledItem,    // قانون 4: شیر ایمنی — چگونه یک شیء را در صورت overflow سقف از بین ببریم
            collectionCheck: true,                  // بررسی اعتبار: اگر کسی تلاش کند یک شیء را دوبار بازگرداند، خطای سختی ایجاد می‌کند
            defaultCapacity: defaultPoolCapacity,   // بلوک پیوسته‌ای از فضا را در کف انبار RAM درست در زمان راه‌اندازی رزرو می‌کند
            maxSize: maxPoolSafetyCeiling          // مرز سخت برای جلوگیری از نشت حافظه و مصرف همه RAM
        );

        // 👑 پارادایم warm-up: موتور را مجبور کنید کارگاه ما را از قبل آماده کند.
        // این تضمین می‌کند cache سخت‌افزار با لینک‌های مرجع aligned پر شده‌اند.
        GameObject[] warmUpBuffer = new GameObject[defaultPoolCapacity];
        for (int i = 0; i < defaultPoolCapacity; i++)
        {
            warmUpBuffer[i] = projectilePool.Get();
        }
        // همه آن‌ها را بلافاصله به کابینت بازگردانید تا برای اکشن بازی آماده باشند
        for (int i = 0; i < defaultPoolCapacity; i++)
        {
            projectilePool.Release(warmUpBuffer[i]);
        }
    }

    void Update()
    {
        // حلقه فریم بدون تخصیص: با صفر heap allocation اجرا می‌شود
        if (Input.GetKey(KeyCode.Space))
        {
            // یک گلوله کاملاً گرم و از پیش بارگذاری‌شده را مستقیماً از حافظه cache بیرون بکشید
            GameObject bullet = projectilePool.Get();
            
            // موقعیت فیزیکی آن را با سرعت از طریق تخصیص مستقیم حافظه بازراه‌اندازی کنید
            bullet.transform.position = firePoint.position;
            bullet.transform.rotation = firePoint.rotation;
        }
    }

    // --- callbacks مدیریت چرخه عمر Pool ---

    private GameObject OnCreatePooledItem()
    {
        // این مسیر فقط در warmup اولیه یا در شرایط استرس بازی اتفاق می‌افتد.
        GameObject instance = Instantiate(projectilePrefab);
        
        // یک token ردیابی وارد کنید تا گلوله بداند دقیقاً به کدام Pool تعلق دارد
        SovereignPooledProjectile token = instance.GetComponent<SovereignPooledProjectile>();
        if (token == null)
        {
            token = instance.AddComponent<SovereignPooledProjectile>();
        }
        
        // handle Pool interface را مستقیماً به رجیسترهای محلی پرتابه بدهید
        token.AssignOriginPool(projectilePool);

        instance.SetActive(false);
        return instance;
    }

    private void OnTakeItemFromPool(GameObject pooledInstance)
    {
        // شیء را دوباره به جهان بازی بازگردانید بدون اینکه initialization سنگین دوباره اجرا شود
        pooledInstance.SetActive(true);
        
        // داده‌های telemtry حرکت را پاک کنید تا مقادیر سرعت قدیمی از بین بروند
        if (pooledInstance.TryGetComponent<Rigidbody>(out var rb))
        {
            rb.linearVelocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
        }
    }

    private void OnReturnItemToPool(GameObject pooledInstance)
    {
        // visuals، physics و مؤلفه‌های پردازشی را بلافاصله غیرفعال کنید.
        // شیء در RAM زنده می‌ماند، اما کاملاً خواب‌آلود می‌شود.
        pooledInstance.SetActive(false);
    }

    private void OnDestroyPooledItem(GameObject pooledInstance)
    {
        // شیر ایمنی فعال شد: اگر بازی در طول انفجار ۱۲۰ گلوله ایجاد کند،
        // اما سقف ما ۱۰۰ باشد، ۲۰ مورد اضافی به‌صورت دائم و تمیز نابود می‌شوند
        // تا مرزهای فیزیکی RAM سخت‌افزار محافظت شوند.
        Destroy(pooledInstance);
    }
}
```

##### 👑 مؤلفه Sovereign Pooled Projectile

```csharp
using UnityEngine;
using UnityEngine.Pool;

public class SovereignPooledProjectile : MonoBehaviour
{
    private IObjectPool<GameObject> originPool;
    private float lifeDurationTracker;
    [SerializeField] private float maxLifeTimeSeconds = 2.0f;

    /// <summary>
    /// این مورد را به Pool اصلی سازمان‌دهنده وصل می‌کند.
    /// </summary>
    public void AssignOriginPool(IObjectPool<GameObject> poolHandle)
    {
        originPool = poolHandle;
    }

    void OnEnable()
    {
        // زمان‌های عمر را هنگام استخراج از کشوی کابینت بازنشانی کنید
        lifeDurationTracker = 0.0f;
    }

    void Update()
    {
        // مدت زمانی را که گلوله در جهان فعال بوده است، رصد کنید
        lifeDurationTracker += Time.deltaTime;
        if (lifeDurationTracker >= maxLifeTimeSeconds)
        {
            ReturnToCabinet();
        }
    }

    void OnCollisionEnter(Collision collision)
    {
        // مداخله فوری در رویدادهای فیزیکی برخورد (مثلاً برخورد با دیوار یا دشمن)
        ReturnToCabinet();
    }

    private void ReturnToCabinet()
    {
        // بررسی کنید که Pool معتبر باشد و شیء قبلاً به خواب نرفته باشد
        if (originPool != null && gameObject.activeSelf)
        {
            // 👑 شاهکار: دوباره به کشوی سیستم برگردانید، نه اینکه Destroy() را فراخوانی کنید.
            // فضای حافظه داغ می‌ماند، اشاره‌گرها تمیز می‌مانند
            // و خط لولهGarbage Collector کاملاً بی‌تأثیر می‌ماند.
            originPool.Release(gameObject);
        }
    }
}
```

---

#### 5. تجزیه و تحلیل معماری و مقایسه

| معیار عملیاتی | معماری تخصیص‌محور ساده | معماری Pool سفارشی با Queue | معماری Pool بومی و پیشرفته Unity |
| --- | --- | --- | --- |
| **تخصیص Heap در زمان اجرا** | **بسیار زیاد** (در هر فریم) | **صفر** (مگر در هنگام تمام شدن Pool) | **صفر** (مگر در هنگام تمام شدن Pool) |
| **تأثیر Garbage Collector** | افت شدید و لرزش‌های میکرو | تأثیر کم (فقط در صورت overrun غیرمنتظره) | **صفر مطلق** (با پیش‌تخصیص warm-up محافظت می‌شود) |
| **محافظت در برابر بازگشت تکراری** | ندارد (اشیاء رها می‌شوند) | ندارد (می‌تواند منجر به خرابی شدید شود) | **عالی** (بررسی مجموعه در زمان اجرا) |
| **مرزهای حافظه** | بدون مرز (می‌تواند تا خرابی RAM ادامه یابد) | مقیاس‌پذیری نامحدود بدون سقف | **سقف ایمنی سخت** (overrun را برای همیشه نابود می‌کند) |
| **هزینه راه‌اندازی** | صفر (همه هزینه‌ها در طول اجرای بازی پرداخت می‌شود) | سربار اولیه کم | بالا (warm-up راه‌اندازی برای ثبات بعدی) |

### [بعدی: فصل ۱۳ انواع سفارشی پیشرفته](/Volume-II-Memory-Mechanics/Chapter-13-Advanced-Custom-Types/FA/)
