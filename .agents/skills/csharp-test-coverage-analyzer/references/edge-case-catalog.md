# Edge Case Catalog for C# Testing

Common edge cases that are frequently missed in test suites.

## Numeric Edge Cases

### Integer Boundaries

```csharp
[Theory]
[InlineData(int.MinValue)]
[InlineData(int.MaxValue)]
[InlineData(0)]
[InlineData(-1)]
[InlineData(1)]
public void ProcessAge_BoundaryValues_HandlesCorrectly(int age)
{
    // Test behavior at extremes
}
```

### Floating Point Issues

```csharp
[Theory]
[InlineData(double.NaN)]
[InlineData(double.PositiveInfinity)]
[InlineData(double.NegativeInfinity)]
[InlineData(double.Epsilon)] // Smallest positive value
[InlineData(-0.0)]
public void Calculate_SpecialFloats_HandlesGracefully(double value)
{
    // Verify NaN, Infinity, and near-zero handling
}

[Fact]
public void SumDecimal_FloatingPointPrecision_IsAccurate()
{
    // 0.1 + 0.2 != 0.3 in floating point
    var result = 0.1m + 0.2m;
    Assert.Equal(0.3m, result); // Use decimal for money
}
```

### Division Edge Cases

```csharp
[Theory]
[InlineData(10, 0)] // Division by zero
[InlineData(int.MinValue, -1)] // Overflow: MinValue / -1 = overflow
[InlineData(0, 0)] // Undefined
public void Divide_ProblematicInputs_ThrowsOrHandles(int a, int b)
{
    // Verify proper exception or special value handling
}
```

## String Edge Cases

### Empty and Null

```csharp
[Theory]
[InlineData(null)]
[InlineData("")]
[InlineData(" ")]
[InlineData("\t\n\r")]
public void ParseName_EmptyOrWhitespace_ReturnsDefault(string input)
{
    // Test null, empty, and whitespace-only strings
}
```

### Special Characters

```csharp
[Theory]
[InlineData("Test\0String")] // Null terminator
[InlineData("Line1\nLine2")] // Newlines
[InlineData("Tab\tSeparated")] // Tabs
[InlineData("Quote\"Test")] // Quotes
[InlineData("Back\\Slash")] // Backslashes
[InlineData("Emoji 😀🎉")] // Unicode
[InlineData("中文字符")] // Non-ASCII
public void ProcessText_SpecialCharacters_HandlesCorrectly(string input)
{
    // Verify special character handling
}
```

### Length Extremes

```csharp
[Fact]
public void SaveComment_MaxLength_Succeeds()
{
    var maxLengthComment = new string('a', 10000);
    var result = _service.SaveComment(maxLengthComment);
    Assert.True(result.Success);
}

[Fact]
public void SaveComment_ExceedsMaxLength_Rejects()
{
    var tooLong = new string('a', 10001);
    Assert.Throws<ArgumentException>(() => _service.SaveComment(tooLong));
}
```

## Collection Edge Cases

### Empty Collections

```csharp
[Fact]
public void ProcessItems_EmptyList_ReturnsEmptyResult()
{
    var result = _processor.Process(new List<Item>());
    Assert.Empty(result);
}

[Fact]
public void GetFirst_EmptyList_ThrowsOrReturnsDefault()
{
    var empty = new List<int>();
    // Verify behavior: exception or default value?
}
```

### Single Element

```csharp
[Fact]
public void Sort_SingleElement_RemainsUnchanged()
{
    var list = new List<int> { 42 };
    _sorter.Sort(list);
    Assert.Single(list);
    Assert.Equal(42, list[0]);
}
```

### Duplicates

```csharp
[Fact]
public void RemoveDuplicates_AllIdentical_ReturnsSingle()
{
    var list = new List<int> { 5, 5, 5, 5, 5 };
    var result = _processor.RemoveDuplicates(list);
    Assert.Single(result);
    Assert.Equal(5, result[0]);
}
```

### Null Elements

```csharp
[Fact]
public void ProcessItems_ContainsNulls_HandlesGracefully()
{
    var list = new List<string> { "valid", null, "also valid", null };
    var result = _processor.Process(list);
    // Verify nulls are filtered or handled
}
```

## Date/Time Edge Cases

### Boundary Dates

```csharp
[Theory]
[InlineData("0001-01-01")] // DateTime.MinValue
[InlineData("9999-12-31")] // DateTime.MaxValue
[InlineData("1970-01-01")] // Unix epoch
[InlineData("2038-01-19")] // 32-bit Unix timestamp overflow
public void ProcessDate_BoundaryValues_HandlesCorrectly(string dateStr)
{
    var date = DateTime.Parse(dateStr);
    var result = _service.ProcessDate(date);
    Assert.NotNull(result);
}
```

### Time Zones

```csharp
[Fact]
public void ConvertTime_CrossesDaylightSaving_HandlesCorrectly()
{
    // Spring forward: 2:00 AM -> 3:00 AM
    var beforeDst = new DateTime(2026, 3, 8, 1, 59, 0);
    var afterDst = beforeDst.AddMinutes(2);
    // Verify DST transition handling
}

[Fact]
public void ScheduleMeeting_DifferentTimeZones_ConvertsCorrectly()
{
    var utcTime = DateTime.UtcNow;
    var tokyoTime = TimeZoneInfo.ConvertTimeBySystemTimeZoneId(utcTime, "Tokyo Standard Time");
    var nyTime = TimeZoneInfo.ConvertTimeBySystemTimeZoneId(utcTime, "Eastern Standard Time");
    // Verify conversions maintain correct moment
}
```

### Leap Years

```csharp
[Theory]
[InlineData(2024, 2, 29)] // Leap year
[InlineData(2023, 2, 28)] // Non-leap year
public void ProcessDate_FebruaryEdges_HandlesCorrectly(int year, int month, int day)
{
    var date = new DateTime(year, month, day);
    var result = _service.ProcessDate(date);
    Assert.NotNull(result);
}

[Fact]
public void AddYear_LeapDayBirthday_HandlesNonLeapYear()
{
    var leapDayBirth = new DateTime(2024, 2, 29);
    var nextYear = leapDayBirth.AddYears(1);
    // Should become Feb 28, 2025 or throw?
}
```

## Concurrency Edge Cases

### Race Conditions

```csharp
[Fact]
public async Task IncrementCounter_Concurrent_AllIncrementsApplied()
{
    var counter = new Counter();
    var tasks = Enumerable.Range(0, 1000)
        .Select(_ => Task.Run(() => counter.Increment()))
        .ToArray();

    await Task.WhenAll(tasks);
    Assert.Equal(1000, counter.Value);
}
```

### Deadlocks

```csharp
[Fact(Timeout = 5000)]
public async Task TransferMoney_ConcurrentBidirectional_NoDeadlock()
{
    var accountA = new Account { Balance = 1000 };
    var accountB = new Account { Balance = 1000 };

    var task1 = Task.Run(() => _service.Transfer(accountA, accountB, 100));
    var task2 = Task.Run(() => _service.Transfer(accountB, accountA, 100));

    await Task.WhenAll(task1, task2); // Should complete without deadlock
}
```

## File System Edge Cases

### Path Issues

```csharp
[Theory]
[InlineData("")]
[InlineData(" ")]
[InlineData("CON")] // Reserved Windows name
[InlineData("file:name.txt")] // Invalid character
[InlineData("verylongname" + new string('a', 300) + ".txt")] // Exceeds limit
public void SaveFile_InvalidPath_ThrowsException(string filename)
{
    Assert.Throws<ArgumentException>(() => _fileService.Save(filename, "content"));
}
```

### File States

```csharp
[Fact]
public void ReadFile_Locked_ThrowsIOException()
{
    // Simulate file locked by another process
    using var stream = File.Open("test.txt", FileMode.Open, FileAccess.Read, FileShare.None);
    Assert.Throws<IOException>(() => _fileService.ReadFile("test.txt"));
}

[Fact]
public void DeleteFile_AlreadyDeleted_HandlesGracefully()
{
    _fileService.DeleteFile("nonexistent.txt");
    // Should not throw or should throw specific exception
}
```

## Network Edge Cases

### Timeouts

```csharp
[Fact(Timeout = 10000)]
public async Task FetchData_ServerNotResponding_TimesOut()
{
    var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
    await Assert.ThrowsAsync<TaskCanceledException>(
        () => _client.GetAsync("http://10.255.255.1", cts.Token));
}
```

### Connection Failures

```csharp
[Fact]
public async Task SendRequest_NetworkDown_RetriesAndFails()
{
    // Simulate network failure
    var result = await _service.SendRequestWithRetry("http://unreachable.test");
    Assert.False(result.Success);
    Assert.Equal(3, result.RetryCount); // Verify retry logic
}
```

## Use This Catalog

When analyzing test coverage, check each relevant category:
1. Identify which edge case categories apply to the code under test
2. Verify tests exist for each applicable edge case
3. Recommend specific missing tests with code examples
4. Prioritize by risk: security > data loss > crashes > incorrect results
