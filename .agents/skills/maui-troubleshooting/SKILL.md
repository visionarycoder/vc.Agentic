---
name: "maui-troubleshooting"
description: ".NET MAUI error diagnosis and fixes: build errors, runtime crashes, MauiDevFlow connection failures, platform-specific issues (iOS/Android/Windows), and UI validation workflows."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MAUI Troubleshooting"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET MAUI Troubleshooting

## Build Errors

### NETSDK1147: Missing workload
```bash
dotnet workload restore
```

### XFC0000: Invalid XAML
Check line number, verify namespaces

### CS0246: Type not found
Add missing `using` or NuGet package

## Runtime Errors

### NullReferenceException in Binding
```csharp
// Set BindingContext BEFORE InitializeComponent
BindingContext = vm;
InitializeComponent();
```

### CollectionView Not Updating
Use `ObservableCollection<T>`, don't replace collection:
```csharp
Items.Clear();
foreach (var item in data)
    Items.Add(item);
```

### Command Not Executing
In DataTemplates, bind to parent:
```xml
<Button Command="{Binding Source={RelativeSource AncestorType={x:Type vm:MainViewModel}}, Path=DeleteCommand}" />
```

### Image Not Displaying
Reference as .png, not .svg:
```xml
<Image Source="icon.png" />
```

### ScrollView Not Scrolling
Put in Grid, not StackLayout:
```xml
<Grid>
    <ScrollView>...</ScrollView>
</Grid>
```

## Performance Issues

### Slow List Scrolling
- Use CollectionView, not ListView
- Put CollectionView in Grid, not StackLayout
- Add x:DataType to DataTemplate
- Simplify item template

### Slow Startup
- Defer work to OnAppearing
- Enable AOT

---

# Platform-Specific Issues

## iOS

### Privacy Descriptions
Add to Info.plist:
```xml
<key>NSCameraUsageDescription</key>
<string>Camera access for photos</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>Photo library access</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Location for nearby places</string>
```

### Signing
1. Xcode → Preferences → Accounts
2. Download profiles
3. In .csproj: `<CodesignKey>Apple Development</CodesignKey>`

### Safe Area
```xml
<ContentPage ios:Page.UseSafeArea="True">
```

## Android

### Permissions
In AndroidManifest.xml:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
```

### Runtime Permissions
```csharp
var status = await Permissions.RequestAsync<Permissions.Camera>();
```

### Install Failed
```bash
adb uninstall com.companyname.myapp
```

### SDK Version
```xml
<SupportedOSPlatformVersion>21</SupportedOSPlatformVersion>
```

## Cross-Platform Code

### Runtime Check
```csharp
if (DeviceInfo.Platform == DevicePlatform.iOS) { }
if (DeviceInfo.Platform == DevicePlatform.Android) { }
```

### Compile-Time Check
```csharp
#if IOS
#elif ANDROID
#elif WINDOWS
#endif
```

### Platform XAML
```xml
<Label FontSize="{OnPlatform iOS=16, Android=14}" />
```

### Idiom
```xml
<Label FontSize="{OnIdiom Phone=14, Tablet=18}" />
```

## Handler Customization

```csharp
EntryHandler.Mapper.AppendToMapping("Custom", (handler, view) =>
{
#if ANDROID
    handler.PlatformView.SetBackgroundColor(Android.Graphics.Color.Transparent);
#elif IOS
    handler.PlatformView.BorderStyle = UIKit.UITextBorderStyle.None;
#endif
});
```

## Main Thread

```csharp
MainThread.BeginInvokeOnMainThread(() =>
{
    // UI updates
});
```

---

## Testing Checklist

### UI Debugging with MauiDevFlow MCP Tools
When debugging UI issues at runtime:
1. Use `maui_tree` to inspect the full visual tree
2. Use `maui_tap` to tap buttons and verify behavior
3. Use `maui_set_property` to test property changes live (colors, visibility, sizes)
4. Use `maui_screenshot` to capture and view visual state (returns actual PNG image)
5. Use `maui_logs` for app log inspection
6. Use `maui_network` to inspect HTTP requests
7. Use `dotnet_maui_getDebugOutput` for raw `Debug.WriteLine`/`Console.WriteLine` output

### MauiDevFlow Connection Failures

When an MCP tool times out, reports no agents, or cannot reach the app:

1. Preserve the exact tool call and first meaningful error.
2. Call `maui_wait` once if the app may still be starting.
3. Call `dotnet_maui_diagnoseDevFlow` before further retries. It works independently of the MCP connection, resolves the selected startup project and active running Android target, and returns CLI, broker, registered agents, exact version mismatches, selected/CLI-discovered project evidence, Android tunnel state, and DevFlow-filtered app output.
4. Treat broker registration and agent reachability separately: `agentCount>0` does not prove the HTTP agent responds.
5. Verify a recovery with `maui_status`, then `maui_tree`.
6. Stop after two identical failures and change the hypothesis.

Load the `maui-devflow-debug` skill for the full failure matrix and platform-specific recovery. Use `maui-devflow-session-review` only after explicit user opt-in.

### Accessibility & Contrast Verification
When verifying color contrast and accessibility:
1. **Query actual rendered colors** — use `maui_get_property` to check `BackgroundColor`, `TextColor`, and `PlaceholderColor` on the control. Do NOT rely on `maui_tree` for color data (it may omit color properties) or on XAML/C# color tokens (they show intent, not what actually renders).
2. **Verify with `maui_assert`** — programmatically check that rendered color values meet contrast expectations.
3. **Visual confirmation** — use `maui_screenshot` if `maui_get_property` returns unexpected values or to confirm the overall visual result. If the screenshot shows poor contrast, it IS poor contrast regardless of what the code says.
4. **⚠️ Platform-native controls** (SearchBar, Entry, Picker, DatePicker, TimePicker) apply their own native styling that can **completely override** XAML color properties. For example, iOS `UISearchBar` renders a dark translucent background regardless of XAML `BackgroundColor`. Always check rendered values on these controls.
5. Aim for **WCAG AA contrast**: 4.5:1 for normal text, 3:1 for large text.

### iOS
- [ ] Real device test
- [ ] Safe area
- [ ] Dark mode
- [ ] Signing valid

### Android
- [ ] Multiple API levels
- [ ] Runtime permissions
- [ ] Back button
- [ ] Screen sizes

### All
- [ ] Offline
- [ ] Orientation
- [ ] Accessibility
