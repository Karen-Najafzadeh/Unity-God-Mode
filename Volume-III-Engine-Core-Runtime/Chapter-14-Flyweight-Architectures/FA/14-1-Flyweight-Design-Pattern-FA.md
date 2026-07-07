<div align="center">

[ Read in English](../14-1-Flyweight-Design-Pattern.md)

</div>

# الگوی طراحی Flyweight: استفاده از ScriptableObject به عنوان بلوپرینت (نقشه) اشتراکی در Unity

### ۱. مقدمه: هنر بلوپرینت اشتراکی

تصور کنید در حال ساخت یک میدان نبرد وسیع با هزاران سرباز، سلاح، دشمن و سیستم‌های رابط کاربری در Unity هستید. اگر هر موجودیت (Entity) نسخه کامل و اختصاصی خود را از پیکربندی‌های سنگین حمل کند، بازی شما تحت فشار داده‌های تکراری، تخصیص حافظه (Allocation) اضافه و ارث‌بری شکننده Prefabها دچار خفگی خواهد شد.

راه حل فقط بهینه‌سازی نیست؛ بلکه حاکمیت معماری است.

الگوی Flyweight به شما می‌آموزد که یک شیء را به دو قلمرو تقسیم کنید:

۱. **حالت ذاتی (Intrinsic State)** — بلوپرینت پایدار و اشتراکی که برای هر نمونه (Instance) هرگز تغییر نمی‌کند.
۲. **حالت بیرونی (Extrinsic State)** — بافتار (Context) منحصربه‌فرد و زمان اجرا که از شیئی به شیء دیگر تغییر می‌کند.

در Unity، قدرتمندترین ابزار بومی برای این مرزبندی، **ScriptableObject** است. یک ScriptableObject فقط یک محفظه داده نیست؛ بلکه یک دارایی (Asset) اشتراکی، یک خزانه در سطح پروژه، یک رجیستری Flyweight و روشی تمیز برای جدا کردن منطق (Logic) از اشیاء صحنه است. اگر MonoBehaviourها بدن‌ها در دنیای بازی هستند، ScriptableObjectها روح‌هایی هستند که در پایگاه داده پروژه ابدی باقی می‌مانند.

---

### ۲. دانش علوم کامپیوتر: بازآفرینی صنعت چاپ

پیش از کامپیوترها، یوهانس گوتنبرگ مشکل مشابهی را حل کرد. اگر یک کاتب می‌خواست ۱۰۰۰ کتاب چاپ کند، کپی کردن دستی تمام حروف کاری بیهوده بود. در عوض، او قالب‌های قابل استفاده مجدد برای هر حرف ایجاد کرد و آن‌ها را در کلمات، صفحات و کتاب‌ها چیدمان کرد.

همین اصل در معماری بازی صدق می‌کند. آمار پایه یک سرباز، پروفایل سلاح، قوانین رفتار دشمن یا متادیتای آیتم‌ها نباید در هر نمونه spawned شده تکرار شوند. آن‌ها باید یک بار ساخته شوند و بارها به آن‌ها ارجاع داده شود.

این ایده Flyweight در یک جمله است: حقیقت سنگین و اشتراکی را در یک مکان نگه دارید و اجازه دهید بسیاری از اشیاء سبک به آن اشاره کنند.

---

### ۳. الگو در کد: یک نمایش اولیه (Bare-Bones)

قبل از بررسی عمیق‌تر، بیایید اصل بنیادی Flyweight را در یک بافتار Unity بدون استفاده از `ScriptableObject` ببینیم:

#### رویکرد ساده‌لوحانه (Naive) (MonoBehaviour)

اگر داده‌های زره را به صورت ساده‌لوحانه بخشی از MonoBehaviour قرار دهیم:

```csharp

public class SoldierNaive : MonoBehaviour
{
    // این فیلدها برای هر نمونه در صحنه تکرار می‌شوند.
    // ۱۰۰۰۰ سرباز = ۱۰۰۰۰ کپی از این داده‌ها در حافظه.
    public string armorName = "Iron Plate";
    public float defenseValue = 50f;
    public float weight = 15f;
    public string material = "Steel";
    public string color = "Grey";
    
    public float currentHealth = 100f;
}
```

#### رویکرد Flyweight دستی (کلاس داده ساده + MonoBehaviour)

```csharp
// ۱. حالت ذاتی (Intrinsic State): داده‌های اشتراکی ذخیره شده در یک کلاس ساده
public class ArmorData
{
    public readonly string armorName;
    public readonly float defenseValue;
    public readonly float weight;
    public readonly string material;
    public readonly string color;

    public ArmorData(string name, float defense, float weight, string material, string color)
    {
        this.armorName = name;
        this.defenseValue = defense;
        this.weight = weight;
        this.material = material;
        this.color = color;
    }
}

// ۲. کارخانه Flyweight (Flyweight Factory): مدیریت نمونه‌های اشتراکی
public static class ArmorFactory
{
    private static System.Collections.Generic.Dictionary<string, ArmorData> _cache = new();

    public static ArmorData GetArmor(string name, float defense, float weight, string material, string color)
    {
        if (!_cache.ContainsKey(name))
            _cache[name] = new ArmorData(name, defense, weight, material, color);
        
        return _cache[name];
    }
}

// ۳. حالت بیرونی (Extrinsic State): استفاده سبک در یک MonoBehaviour
public class SoldierFlyweight : MonoBehaviour
{
    // ارجاع به داده‌های اشتراکی (ذاتی)
    public ArmorData armorProfile; 
    
    // حالت اختصاصی نمونه (بیرونی)
    public float currentHealth = 100f;

    // متد کارخانه برای مقداردهی اولیه (اغلب توسط یک اسکریپت spawner فراخوانی می‌شود)
    public void Initialize(ArmorData data)
    {
        this.armorProfile = data;
    }
}
```

#### تأثیر بر حافظه

| جنبه | ساده‌لوحانه (Naive) | Flyweight |
|--------|-------|-----------|
| **کپی‌های پیکربندی اشتراکی** | ۱۰۰۰۰ | ۱ |
| **حالت منحصربه‌فرد برای هر سرباز** | همچنان مورد نیاز | همچنان مورد نیاز |
| **ردپای حافظه** | رشد $O(N)$ | نزدیک به ثابت |
| **پچ تعادل** | ویرایش ۱۰۰۰۰ شیء | ویرایش ۱ بلوپرینت |

این پایه و اساس است. شیء منبع حقیقت نیست، بلوپرینت منبع حقیقت است. بسیاری از ارجاعات سبک به یک مرجع اشتراکی اشاره دارند. این کل الگو است.

---

### ۴. چرا روش قدیمی شکست می‌خورد: مالیات MonoBehaviour

معماری ساده‌لوحانه در Unity اغلب همه چیز را روی یک MonoBehaviour متصل به یک Prefab قرار می‌دهد:

```csharp
using UnityEngine;

public class NaiveWeaponEntity : MonoBehaviour
{
    public string weaponName;
    public string description;
    public float baseDamage;
    public float attackSpeed;
    public byte[] highResTextureMatrix;
    public AudioClip swingSound;
    public GameObject impactParticlePrefab;

    public float currentDurability;
    public int currentItemLevel;
}
```

این کد تا زمانی که صدها یا هزاران کپی از آن spawn نکنید، بی‌خطر به نظر می‌رسد. هر نمونه اکنون کپی خاص خود را از همان داده‌های پیکربندی حمل می‌کند. هرچه بیشتر کلون کنید، نمایه حافظه شما بیشتر باد می‌کند.

فاجعه پنهان فقط حافظه نیست؛ بلکه قابلیت نگهداری (Maintainability) است:

- تغییر یک مقدار تعادل به معنای ویرایش کپی‌های زیاد یا Prefabهای زیاد است.
- بارگذاری مجدد صحنه می‌تواند وضعیت زمان اجرا را پاک کند، مگر اینکه آن را به صورت دستی سریال کنید.
- Prefabها حجیم و شکننده می‌شوند.
- داده‌ها به شدت به شیء بصری جوش می‌خورند، که معماری شما را کمتر قابل استفاده مجدد می‌کند.

---

### ۴. نجات معماری: ScriptableObjects به عنوان خزانه اشتراکی

یک ScriptableObject به شما اجازه می‌دهد داده‌های ذاتی را از شیء صحنه خارج کرده و به یک دارایی پروژه منتقل کنید.

این شکل بومی Unity از الگوی Flyweight است.

به جای ذخیره بلوپرینت اشتراکی روی هر دشمن، شمشیر یا نمونه آیتم، شما یک دارایی واحد در پروژه خود ایجاد می‌کنید و اجازه می‌دهید هر موجودیت به آن ارجاع دهد.

نتیجه عمیق است:

- یک دارایی پیکربندی می‌تواند به هزاران موجودیت زمان اجرا خدمت کند.
- ویرایش یک دارایی، حقیقت اشتراکی را در سراسر بازی به‌روزرسانی می‌کند.
- Instantiation سبک، سریع و ارزان می‌شود.
- اشیاء صحنه شما به محفظه‌های سبک زمان اجرا تبدیل می‌شوند، نه انبارهای داده.

---

### ۵. مرز بزرگ: چه چیزی متعلق به دارایی است و چه چیزی متعلق به شیء

یک خدای Unity (Unity God) باید این قانون را به وضوح درک کند:

- داده‌های اشتراکی، پایدار و تکراری را روی یک ScriptableObject قرار دهید.
- وضعیت منحصربه‌فرد هر شیء را روی یک MonoBehaviour یا کامپوننت زمان اجرا قرار دهید.

مثال‌های خوب:

- اشتراکی: آمار سلاح، داده‌های کهن‌الگوی دشمن، تعاریف آیتم‌های سطح، کانال‌های رویداد، پیکربندی UI، متغیرهای بازی قابل استفاده مجدد.
- منحصربه‌فرد: سلامتی فعلی، موقعیت فعلی، وضعیت انیمیشن، زمان‌های خنک‌کننده (Cooldown) زمان اجرا، تعداد موجودی محلی، وضعیت خاص صحنه.

این قانون پنهان معماری است: دارایی حقیقت است، کامپوننت بافتار (Context) است.

---

### ۶. پیاده‌سازی هسته: دارایی داده اشتراکی + بازیگر سبک

#### بلوپرینت اشتراکی

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewWeaponConfig", menuName = "SovereignEngine/Weapon Configuration")]
public class WeaponDataConfig : ScriptableObject
{
    [SerializeField] private string weaponName;
    [SerializeField] private float baseDamage;
    [SerializeField] private float attackSpeed;
    [SerializeField] private AudioClip swingSound;
    [SerializeField] private GameObject impactParticlePrefab;

    public string WeaponName => weaponName;
    public float BaseDamage => baseDamage;
    public float AttackSpeed => attackSpeed;
    public AudioClip SwingSound => swingSound;
    public GameObject ImpactParticlePrefab => impactParticlePrefab;
}
```

#### موجودیت سبک زمان اجرا

```csharp
using UnityEngine;

public class WorldWeaponEntity : MonoBehaviour
{
    [SerializeField] private WeaponDataConfig configuration;

    public float currentDurability;
    public bool isEnchanted;

    public void ExecuteAttack()
    {
        Debug.Log($"Attacking with {configuration.WeaponName} dealing {configuration.BaseDamage} damage!");

        if (configuration.SwingSound != null)
        {
            AudioSource.PlayClipAtPoint(configuration.SwingSound, transform.position);
        }

        if (configuration.ImpactParticlePrefab != null)
        {
            Instantiate(configuration.ImpactParticlePrefab, transform.position, Quaternion.identity);
        }
    }
}
```

این معماری Flyweight به خالص‌ترین شکل خود است: یک دارایی پیکربندی اشتراکی، بسیاری از اشیاء سبک دنیای بازی که به آن اشاره می‌کنند.

---

### ۷. راز پنهان: ScriptableObjects فراتر از فروشگاه‌های داده هستند

بیشتر توسعه‌دهندگان فکر می‌کنند ScriptableObjectها فقط «متغیرهای اشتراکی» هستند. این فقط سطح ماجرا است.

آن‌ها در واقع سه چیز هستند:

۱. **یک دارایی داده** — یک شیء سریال شده ذخیره شده در پروژه.
۲. **یک کانال ارتباطی** — یک هاب مرکزی که بسیاری از سیستم‌ها می‌توانند در آن مشترک شوند.
۳. **یک ابزار جداسازی (Decoupling)** — راهی برای اینکه سیستم‌ها بدون ارجاع مستقیم به یکدیگر با هم صحبت کنند.

این یعنی یک ScriptableObject می‌تواند پایه و اساس این موارد باشد:

- رجیستری‌های کهن‌الگوی دشمن،
- تعاریف موجودی،
- پایگاه‌های داده دیالوگ،
- رویدادهای جهانی،
- محفظه‌های وضعیت زمان اجرا،
- جداول تعادل گیم‌پلی،
- پیکربندی‌های مبتنی بر ادیتور.

به همین دلیل است که آن‌ها در پروژه‌های بزرگ Unity بسیار قدرتمند هستند.

---

### ۸. واقعیت شگفت‌انگیز: یک دارایی می‌تواند کل یک ارتش را تغذیه کند

اگر یک دارایی پیکربندی دشمن واحد ایجاد کنید و اجازه دهید ۱۰۰۰۰ واحد spawned شده به آن اشاره کنند، نه تنها در حافظه صرفه‌جویی می‌کنید. بلکه هندسه معماری خود را تغییر می‌دهید.

رویکرد قدیمی به صورت خطی با هر نمونه مقیاس می‌شود. رویکرد Flyweight نزدیک به ثابت باقی می‌ماند زیرا داده‌های سنگین اشتراکی تکرار نمی‌شوند.

این جهش واقعی است:

- معماری ساده‌لوحانه: رشد حافظه $O(N)$ به ازای هر نمونه.
- معماری Flyweight: هزینه بلوپرینت اشتراکی نزدیک به $O(1)$.

یک خدای Unity صرفاً کارها را انجام نمی‌دهد. یک خدای Unity باعث مقیاس‌پذیری آن‌ها می‌شود.

---

### ۹. الگوی کانال رویداد: جداسازی بدون Singletons

یکی از خطرناک‌ترین عادت‌ها در Unity استفاده بیش از حد از Singletonها است. آن‌ها وابستگی‌های پنهان در همه جا ایجاد می‌کنند. یک ScriptableObject می‌تواند با عمل کردن به عنوان یک گذرگاه رویداد جهانی (Global Event Bus)، این مشکل را با ظرافت بیشتری حل کند.

```csharp
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "NewGameEvent", menuName = "SovereignEngine/Architecture/Game Event")]
public class SovereignGameEvent : ScriptableObject
{
    private readonly List<SovereignEventListener> listeners = new List<SovereignEventListener>();

    public void Raise()
    {
        for (int i = listeners.Count - 1; i >= 0; i--)
        {
            listeners[i].OnEventRaised();
        }
    }

    public void RegisterListener(SovereignEventListener listener)
    {
        if (!listeners.Contains(listener)) listeners.Add(listener);
    }

    public void UnregisterListener(SovereignEventListener listener)
    {
        if (listeners.Contains(listener)) listeners.Remove(listener);
    }
}
```

```csharp
using UnityEngine;
using UnityEngine.Events;

public class SovereignEventListener : MonoBehaviour
{
    [SerializeField] private SovereignGameEvent eventChannel;
    [SerializeField] private UnityEvent responseAction;

    private void OnEnable()
    {
        if (eventChannel != null) eventChannel.RegisterListener(this);
    }

    private void OnDisable()
    {
        if (eventChannel != null) eventChannel.UnregisterListener(this);
    }

    public void OnEventRaised()
    {
        responseAction?.Invoke();
    }
}
```

این یک تغییر معماری شگفت‌انگیز است. بازیکن می‌تواند یک رویداد بازی را بدون اینکه بداند چه کسی در حال گوش دادن است، فعال کند. رابط کاربری، صدا، هوش مصنوعی و تحلیلگرها همه می‌توانند بدون وابستگی شدید (Tight Coupling) واکنش نشان دهند.

---

### ۱۰. راز پنهان: متغیرهای اشتراکی قدرتمند هستند، اما در صورت استفاده نادرست خطرناک هستند

شما همچنین می‌توانید از ScriptableObjectها به عنوان محفظه‌های وضعیت زمان اجرای اشتراکی استفاده کنید:

```csharp
using UnityEngine;

[CreateAssetMenu(fileName = "NewSharedFloat", menuName = "SovereignEngine/Variables/Shared Float")]
public class SharedFloatVariable : ScriptableObject
{
    [SerializeField] private float value;

    public float Value
    {
        get => value;
        set => this.value = value;
    }
}
```

این برای داده‌های بین‌سیستمی مانند سلامتی، مانا، دشواری یا وضعیت مأموریت مفید است. اما یک تله پنهان وجود دارد:

- اگر همه چیز را به یک متغیر اشتراکی تبدیل کنید، بازی شما به شبکه‌ای از وضعیت‌های جهانی تبدیل می‌شود.
- داده‌های قابل تغییر اشتراکی می‌توانند وابستگی‌های سخت برای دیباگ ایجاد کنند.
- ScriptableObjectها سیستم‌های ذخیره (Save) جادویی نیستند.

نظم این است: از آن‌ها برای حقایق اشتراکی و آگاهانه جهانی استفاده کنید، نه برای هر تکه کوچک از وضعیت محلی.

---

### ۱۱. الگوی یکپارچه: Flyweight در یک نمودار باشکوه

یک خدای Unity باید به این ترتیب فکر کند:

۱. شناسایی کنید که چه داده‌ای واقعاً اشتراکی است.
۲. آن داده را به یک دارایی ScriptableObject منتقل کنید.
۳. شیء زمان اجرا را باریک و بافتارمند (Contextual) نگه دارید.
۴. اجازه دهید بسیاری از اشیاء به آن یک دارایی اشتراکی اشاره کنند.
۵. از دارایی به عنوان کانالی برای ارتباط و پیکربندی استفاده کنید.

این معماری کامل است.

---

### ۱۲. حکمت نهایی: قانون خدای Unity

اگر در حال ساخت یک پروژه جدی هستید، هرگز اجازه ندهید اشیاء صحنه شما به انبارهای داده تبدیل شوند.

اجازه دهید آن‌ها باشند:

- محفظه‌ها،
- کنترل‌کننده‌ها،
- لایه‌های تعامل،
- دارندگان وضعیت زمان اجرا.

اجازه دهید دارایی‌های شما باشند:

- بلوپرینت‌ها،
- رجیستری‌ها،
- تعاریف،
- کانال‌ها،
- حقایق اشتراکی.

این راز پنهان معماری با کارایی بالا در Unity است. شیء منبع حقیقت نیست. دارایی منبع حقیقت است.

و هنگامی که این را درک کنید، بازی شما از توده‌ای از اشیاء تکراری به سیستمی از هوش ظریف، اشتراکی و مقیاس‌پذیر تبدیل می‌شود.


### [بعدی: معماری طراحی‌های داده (Architecture of Data Layouts)](./14-2-Architecture-of-Data-Layouts-FA.md)
