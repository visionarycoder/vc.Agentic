using System;
using Ifx.Component;
using Microsoft.Extensions.Logging;

namespace Agentic.Samples.Components;

/// <summary>Illustrates component initialization with a typed base logger.</summary>
/// <param name="loggerFactory">The factory used to create the component logger.</param>
public class OrderManager(ILoggerFactory loggerFactory)
    : ComponentBase<OrderManager>(
        (loggerFactory ?? throw new ArgumentNullException(nameof(loggerFactory)))
            .CreateLogger<OrderManager>()),
      IOrderManager
{
}
