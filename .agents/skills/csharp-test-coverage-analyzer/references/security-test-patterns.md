# Security Test Patterns for C#

This reference covers common security vulnerabilities and how to test for them in C# applications.

## Input Validation Testing

### SQL Injection

```csharp
[Theory]
[InlineData("'; DROP TABLE Users; --")]
[InlineData("1' OR '1'='1")]
[InlineData("admin'--")]
public void UserQuery_MaliciousSqlInput_ThrowsOrSanitizes(string input)
{
    // Verify parameterized queries prevent injection
    var result = _repository.GetUser(input);
    // Should either throw ArgumentException or return null safely
}
```

### XSS (Cross-Site Scripting)

```csharp
[Theory]
[InlineData("<script>alert('xss')</script>")]
[InlineData("<img src=x onerror=alert('xss')>")]
[InlineData("javascript:alert('xss')")]
public void RenderContent_MaliciousHtml_IsEscaped(string input)
{
    var output = _renderer.RenderUserContent(input);
    Assert.DoesNotContain("<script>", output);
    Assert.DoesNotContain("onerror=", output);
}
```

### Path Traversal

```csharp
[Theory]
[InlineData("../../../etc/passwd")]
[InlineData("..\\..\\..\\windows\\system32\\config\\sam")]
[InlineData("file:///etc/passwd")]
public void ReadFile_PathTraversalAttempt_ThrowsSecurityException(string path)
{
    Assert.Throws<SecurityException>(() => _fileService.ReadFile(path));
}
```

## Authentication & Authorization

### Unauthenticated Access

```csharp
[Fact]
public void ProtectedEndpoint_NoAuthToken_Returns401()
{
    var response = _client.GetAsync("/api/admin/users").Result;
    Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
}
```

### Privilege Escalation

```csharp
[Fact]
public void AdminEndpoint_RegularUserToken_Returns403()
{
    _client.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer", _regularUserToken);
    var response = _client.GetAsync("/api/admin/users").Result;
    Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
}
```

### Token Tampering

```csharp
[Theory]
[InlineData("eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbiJ9.")] // Algorithm: none
[InlineData("tampered.token.value")]
public void ValidateToken_TamperedToken_ReturnsFalse(string token)
{
    var result = _tokenValidator.Validate(token);
    Assert.False(result.IsValid);
}
```

## Cryptography

### Weak Encryption

```csharp
[Fact]
public void EncryptPassword_UsesStrongAlgorithm()
{
    var encrypted = _crypto.EncryptPassword("password123");
    // Verify NOT using MD5, SHA1, or DES
    Assert.DoesNotContain("MD5", _crypto.GetAlgorithmName());
    Assert.DoesNotContain("SHA1", _crypto.GetAlgorithmName());
}
```

### Insufficient Randomness

```csharp
[Fact]
public void GenerateToken_ProducesUnpredictableValues()
{
    var tokens = Enumerable.Range(0, 1000)
        .Select(_ => _tokenGenerator.Generate())
        .ToList();

    // All tokens should be unique
    Assert.Equal(1000, tokens.Distinct().Count());

    // Should not be sequential or patterned
    Assert.False(AreSequential(tokens));
}
```

## Sensitive Data Exposure

### Logging Sensitive Data

```csharp
[Fact]
public void LogUserAction_DoesNotLogPassword()
{
    var logOutput = new StringWriter();
    _logger.AddProvider(new StringLoggerProvider(logOutput));

    _userService.Login("user@example.com", "SecretPassword123");

    var logs = logOutput.ToString();
    Assert.DoesNotContain("SecretPassword123", logs);
    Assert.DoesNotContain("password", logs, StringComparison.OrdinalIgnoreCase);
}
```

### API Response Leakage

```csharp
[Fact]
public void GetUser_DoesNotExposeInternalIds()
{
    var response = _api.GetUser("user123");
    var json = JsonSerializer.Serialize(response);

    // Should not expose internal database IDs, hashes, etc.
    Assert.DoesNotContain("InternalId", json);
    Assert.DoesNotContain("PasswordHash", json);
}
```

## Denial of Service (DoS)

### Resource Exhaustion

```csharp
[Fact]
public void ProcessUpload_ExcessiveSize_Rejects()
{
    var hugeFile = new byte[100_000_000]; // 100 MB
    Assert.Throws<FileSizeLimitExceededException>(
        () => _uploadService.ProcessFile(hugeFile));
}

[Fact]
public void ParseXml_BillionLaughsAttack_TimesOut()
{
    var maliciousXml = @"<?xml version=""1.0""?>
        <!DOCTYPE lolz [
          <!ENTITY lol ""lol"">
          <!ENTITY lol2 ""&lol;&lol;&lol;&lol;"">
          <!ENTITY lol3 ""&lol2;&lol2;&lol2;&lol2;"">
        ]>
        <lolz>&lol3;</lolz>";

    Assert.Throws<XmlException>(() => _parser.Parse(maliciousXml));
}
```

## Race Conditions

### TOCTOU (Time-of-Check Time-of-Use)

```csharp
[Fact]
public async Task ConcurrentWithdraw_InsufficientFunds_OnlyOneSucceeds()
{
    var account = new Account { Balance = 100 };

    var tasks = Enumerable.Range(0, 10)
        .Select(_ => Task.Run(() => account.Withdraw(100)))
        .ToArray();

    await Task.WhenAll(tasks);

    // Only one withdrawal should succeed
    var successCount = tasks.Count(t => t.Result == true);
    Assert.Equal(1, successCount);
    Assert.Equal(0, account.Balance);
}
```

## Security Test Checklist

When analyzing tests for security gaps, verify coverage of:

- [ ] All user input validation
- [ ] Authentication bypass attempts
- [ ] Authorization boundary violations
- [ ] Cryptographic operations use strong algorithms
- [ ] Sensitive data never logged or exposed
- [ ] File operations validate paths
- [ ] Resource limits enforced (size, rate, time)
- [ ] Concurrent access to shared state
- [ ] Error messages don't leak internal details
- [ ] Session management (timeout, invalidation)
