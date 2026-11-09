---
name: "maui-development"
description: ".NET MAUI UI development: XAML patterns, MVVM with CommunityToolkit.Mvvm, layout examples, and performance optimization. Use when creating or modifying MAUI UI, writing XAML, implementing ViewModels, or optimizing performance."
metadata:
  metadata-version: "1.0.0"
  title: ".NET MAUI Development"
  document-type: "skill"
  repository: "vc.Agentic"
  language: "Standard Technical English"
  updated: "2026-11-08"
  collection: "dotnet"
---

# .NET MAUI Development

## Layout Controls

### Grid
```xml
<Grid RowDefinitions="Auto,*,Auto" ColumnDefinitions="*,2*">
    <Label Grid.Row="0" Text="Header" />
    <CollectionView Grid.Row="1" Grid.ColumnSpan="2" />
    <Button Grid.Row="2" Grid.Column="1" Text="Submit" />
</Grid>
```

### Border (Preferred over Frame)
```xml
<Border Stroke="{StaticResource Gray300}"
        StrokeThickness="1"
        StrokeShape="RoundRectangle 8"
        Padding="16">
    <Label Text="Content" />
</Border>
```

### ScrollView (Must be in Grid)
```xml
<Grid>
    <ScrollView>
        <VerticalStackLayout Padding="16">
            <!-- Content -->
        </VerticalStackLayout>
    </ScrollView>
</Grid>
```

## Data Display

### CollectionView
```xml
<CollectionView ItemsSource="{Binding Items}">
    <CollectionView.ItemTemplate>
        <DataTemplate x:DataType="models:Item">
            <Border Padding="12">
                <Label Text="{Binding Name}" />
            </Border>
        </DataTemplate>
    </CollectionView.ItemTemplate>
    <CollectionView.EmptyView>
        <Label Text="No items" HorizontalOptions="Center" />
    </CollectionView.EmptyView>
</CollectionView>
```

### BindableLayout (≤20 items)
```xml
<VerticalStackLayout BindableLayout.ItemsSource="{Binding SmallList}">
    <BindableLayout.ItemTemplate>
        <DataTemplate x:DataType="models:Item">
            <Label Text="{Binding Name}" />
        </DataTemplate>
    </BindableLayout.ItemTemplate>
</VerticalStackLayout>
```

## Input Controls

```xml
<Entry Placeholder="Email" Text="{Binding Email}" Keyboard="Email" />
<Editor Text="{Binding Description}" AutoSize="TextChanges" />
<Picker ItemsSource="{Binding Options}" SelectedItem="{Binding Selected}" />
<Switch IsToggled="{Binding IsEnabled}" />
<Slider Minimum="0" Maximum="100" Value="{Binding Progress}" />
<DatePicker Date="{Binding SelectedDate}" />
<SearchBar Text="{Binding SearchText}" SearchCommand="{Binding SearchCommand}" />
```

## Interactive Controls

### RefreshView
```xml
<RefreshView IsRefreshing="{Binding IsRefreshing}" Command="{Binding RefreshCommand}">
    <CollectionView ItemsSource="{Binding Items}" />
</RefreshView>
```

### SwipeView
```xml
<SwipeView>
    <SwipeView.RightItems>
        <SwipeItems>
            <SwipeItem Text="Delete" Background="Red" Command="{Binding DeleteCommand}" />
        </SwipeItems>
    </SwipeView.RightItems>
    <Label Text="{Binding Name}" />
</SwipeView>
```

## Images (Always .png)

```xml
<Image Source="icon.png" Aspect="AspectFit" />
```

---

# XAML Patterns

## Page Template

```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.MyPage"
             x:DataType="vm:MyViewModel"
             Title="{Binding Title}">

    <Grid RowDefinitions="Auto,*,Auto">
        <Label Grid.Row="0" Text="Header" />
        <ScrollView Grid.Row="1">
            <VerticalStackLayout Padding="16" Spacing="8">
                <!-- Content -->
            </VerticalStackLayout>
        </ScrollView>
        <Button Grid.Row="2" Text="Action" Command="{Binding ActionCommand}" />
    </Grid>
</ContentPage>
```

## Compiled Bindings (Required)

```xml
<!-- Page level -->
<ContentPage x:DataType="vm:MainViewModel">
    <Label Text="{Binding Title}" />
</ContentPage>

<!-- DataTemplate (REQUIRED) -->
<DataTemplate x:DataType="models:Item">
    <Label Text="{Binding Name}" />
</DataTemplate>
```

## Binding Modes

```xml
<Label Text="{Binding Id, Mode=OneTime}" />      <!-- Static data -->
<Label Text="{Binding Name}" />                   <!-- Read-only (default) -->
<Entry Text="{Binding Name, Mode=TwoWay}" />      <!-- Editable -->
```

## Binding to Parent (in DataTemplates)

```xml
<Button Command="{Binding Source={RelativeSource AncestorType={x:Type vm:MainViewModel}}, Path=DeleteCommand}"
        CommandParameter="{Binding}" />
```

## String Formatting

```xml
<Label Text="{Binding Price, StringFormat='Price: {0:C}'}" />
<Label Text="{Binding Date, StringFormat='{0:MMM dd, yyyy}'}" />
```

## Resources & Styles

```xml
<Application.Resources>
    <Color x:Key="Primary">#512BD4</Color>

    <!-- Implicit (auto-applied) -->
    <Style TargetType="Button">
        <Setter Property="Background" Value="{StaticResource Primary}" />
    </Style>

    <!-- Explicit (must reference) -->
    <Style x:Key="HeaderLabel" TargetType="Label">
        <Setter Property="FontSize" Value="24" />
    </Style>
</Application.Resources>

<Label Style="{StaticResource HeaderLabel}" />
```

## Data Triggers

```xml
<Button Text="Submit">
    <Button.Triggers>
        <DataTrigger TargetType="Button" Binding="{Binding IsValid}" Value="False">
            <Setter Property="IsEnabled" Value="False" />
            <Setter Property="Opacity" Value="0.5" />
        </DataTrigger>
    </Button.Triggers>
</Button>
```

## Common Patterns

### Loading State
```xml
<Grid>
    <ScrollView IsVisible="{Binding IsNotBusy}">
        <!-- Content -->
    </ScrollView>
    <ActivityIndicator IsRunning="{Binding IsBusy}" IsVisible="{Binding IsBusy}" />
</Grid>
```

### Empty State
```xml
<CollectionView.EmptyView>
    <VerticalStackLayout HorizontalOptions="Center" VerticalOptions="Center">
        <Label Text="No items found" />
        <Button Text="Add Item" Command="{Binding AddCommand}" />
    </VerticalStackLayout>
</CollectionView.EmptyView>
```

---

# MVVM with CommunityToolkit.Mvvm

## ViewModel Pattern

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class MainViewModel : ObservableObject
{
    private readonly IMyService _service;

    public MainViewModel(IMyService service)
    {
        _service = service;
    }

    [ObservableProperty]
    private string _title = "Welcome";

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(IsNotBusy))]
    private bool _isBusy;

    public bool IsNotBusy => !IsBusy;

    [RelayCommand]
    private async Task LoadAsync()
    {
        if (IsBusy) return;
        try
        {
            IsBusy = true;
            await _service.LoadAsync();
        }
        finally
        {
            IsBusy = false;
        }
    }
}
```

## Observable Properties

```csharp
[ObservableProperty]
private string _name = string.Empty;

// Dependent property
[ObservableProperty]
[NotifyPropertyChangedFor(nameof(FullName))]
private string _firstName = string.Empty;

public string FullName => $"{FirstName} {LastName}";

// Change callback
partial void OnSearchTextChanged(string value)
{
    FilterItems(value);
}

// CanExecute notification
[ObservableProperty]
[NotifyCanExecuteChangedFor(nameof(SubmitCommand))]
private string _email = string.Empty;
```

## Commands

```csharp
[RelayCommand]
private void Increment() => Count++;

[RelayCommand]
private async Task RefreshAsync() => await LoadAsync();

[RelayCommand]
private void Select(Item item) => Selected = item;

[RelayCommand(CanExecute = nameof(CanSubmit))]
private async Task SubmitAsync() { }

private bool CanSubmit() => !string.IsNullOrWhiteSpace(Email);
```

## Dependency Injection

```csharp
// MauiProgram.cs
builder.Services.AddSingleton<IMyService, MyService>();
builder.Services.AddTransient<MainViewModel>();
builder.Services.AddTransient<MainPage>();

// Page
public partial class MainPage : ContentPage
{
    public MainPage(MainViewModel vm)
    {
        BindingContext = vm;
        InitializeComponent();
    }
}
```

## Shell Navigation

```csharp
// Register routes
Routing.RegisterRoute(nameof(DetailPage), typeof(DetailPage));

// Navigate
await Shell.Current.GoToAsync($"{nameof(DetailPage)}?id={item.Id}");
await Shell.Current.GoToAsync(".."); // Back

// Receive parameters
[QueryProperty(nameof(ItemId), "id")]
public partial class DetailViewModel : ObservableObject
{
    [ObservableProperty]
    private string _itemId = string.Empty;

    partial void OnItemIdChanged(string value) => LoadCommand.Execute(null);
}
```

## Collections

```csharp
[ObservableProperty]
private ObservableCollection<Item> _items = new();

[RelayCommand]
private async Task LoadItemsAsync()
{
    var data = await _service.GetItemsAsync();
    Items.Clear();
    foreach (var item in data)
        Items.Add(item);
}
```

## Messaging

```csharp
// Message
public record ItemAddedMessage(Item Item);

// Send
WeakReferenceMessenger.Default.Send(new ItemAddedMessage(item));

// Receive
public partial class MyViewModel : ObservableObject, IRecipient<ItemAddedMessage>
{
    public MyViewModel() => WeakReferenceMessenger.Default.Register(this);
    public void Receive(ItemAddedMessage msg) => Items.Add(msg.Item);
}
```

---

# Performance

## Startup Performance

```csharp
// Defer work to OnAppearing
protected override async void OnAppearing()
{
    base.OnAppearing();
    await ViewModel.LoadCommand.ExecuteAsync(null);
}
```

## Memory Management

```csharp
// Unsubscribe events
protected override void OnDisappearing()
{
    base.OnDisappearing();
    MyService.DataChanged -= OnDataChanged;
}
```

## Binding Tips

```xml
<!-- OneTime for static data -->
<Label Text="{Binding UserId, Mode=OneTime}" />

<!-- Don't bind static values -->
<Label Text="My App" />  <!-- Not {Binding AppName} -->
```

## Performance Checklist

- [ ] Events unsubscribed
- [ ] AOT enabled for Release
