# Naming and Quality Rule Details

Extended guidance for naming-related CA/CS diagnostics in roslyn-ca-code-quality-fixes.

## CA1711: Rename types to avoid reserved suffixes

**Detection:** Type name ends with reserved suffix like `Delegate`, `Enum`, `Impl`, `Ex`

**Fix:** Rename type with proper semantic name. For public APIs: Add `[Obsolete]` shim.

## CA1716: Rename identifiers to avoid language keyword conflicts

**Detection:** Member/type name matches reserved keyword in VB/F#

**Fix:** Rename to non-keyword identifier. Common conflicts: `Property`, `Shared`, `Module`

## CA1720: Identifier contains type name

**Detection:** Variable/property name contains primitive type like `Int`, `String`, `Bool`

**Fix:** Rename with semantic intent. `stringLength` → `length`, `guidValue` → `identifier`

## CA1725: Parameter name does not match base declaration

**Detection:** Method parameter name differs from base class or interface parameter

**Fix:** Rename to match base member signature for IntelliSense consistency.

## CA1727: Use PascalCase for named placeholders

**Detection:** Logging template uses non-PascalCase placeholder like `{userId}`, `{order_id}`

**Fix:** Rename to PascalCase: `{UserId}`, `{OrderId}`

## CA2201: Do not raise reserved exception types

**Detection:** Throws `Exception`, `SystemException`, `ApplicationException`

**Fix:** Use specific types: `InvalidOperationException`, `ArgumentException`, `KeyNotFoundException`

## CS0108: Member hides inherited member

**Detection:** Derived member hides base member without `new` modifier

**Fix:** Add `new` modifier or rename to avoid hiding.

## CS0168/CS0169/CS0219/CS0414: Unused warnings

**Detection:** Variable/field declared/assigned but never read

**Fix:** Remove if unused, use `_` discard for side effects, verify reflection activation.

## CS1717: Assignment made to same variable

**Detection:** `x = x;`

**Fix:** Remove redundant assignment. Check for copy/paste error.

## CS9113: Primary constructor parameter not used

**Detection:** Primary constructor parameter not captured or used

**Fix:** Remove parameter, use in initialization, or suppress with justification.
