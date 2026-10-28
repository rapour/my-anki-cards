This Istio `EnvoyFilter` is applied to an Azure Kubernetes Service (AKS) cluster. What does it do, and what does each part mean?

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: hsts
  namespace: aks-istio-ingress
spec:
  workloadSelector:
    labels:
      istio: aks-istio-ingressgateway-external
  configPatches:
    - applyTo: ROUTE_CONFIGURATION
      match:
        context: GATEWAY
        routeConfiguration:
          portNumber: 443
      patch:
        operation: MERGE
        value:
          response_headers_to_add:
            - append_action: ADD_IF_ABSENT
              header:
                key: Strict-Transport-Security
                value: max-age=31536000
```

---

It adds the **HSTS header** to every HTTPS response leaving the cluster's **external ingress gateway**, so no application has to set it. HSTS is the header `Strict-Transport-Security: max-age=31536000`. It tells browsers to use only HTTPS for that host for the next year, which stops attackers from keeping users on plain HTTP.

Background: the **ingress gateway** is an Envoy proxy at the edge of the cluster that receives outside traffic and routes it to services. An `EnvoyFilter` patches that proxy's generated configuration directly.

| Part | Meaning |
|---|---|
| `workloadSelector: istio: aks-istio-ingressgateway-external` | Patch only the gateway pods with this label: the external gateway of the AKS Istio add-on, not the internal gateway or the services' sidecars |
| `applyTo: ROUTE_CONFIGURATION` | Patch a route configuration: the table that maps host names and paths to services for one listener |
| `context: GATEWAY`, `portNumber: 443` | Pick the gateway's route configuration for its HTTPS port, 443. That is the right place, because browsers ignore the header over plain HTTP |
| `operation: MERGE` with `response_headers_to_add` | Add the header to every response served through those routes |
| `append_action: ADD_IF_ABSENT` | Add it only if the response doesn't already carry one, so an application can still send its own value, such as one with `includeSubDomains` |

Check it from outside:

```sh
curl -sI https://<your-host>/ | grep -i strict-transport-security
```

**Things it doesn't do:**

- **No HTTP-to-HTTPS redirect.** First-time visitors on port 80 still need one, for example `tls.httpsRedirect: true` on the Istio `Gateway`'s port 80 server.
- **No header on TLS passthrough hosts.** If a host on 443 uses passthrough, the gateway forwards encrypted bytes without reading HTTP, so it can't add headers.
- **Exact host only.** Without `includeSubDomains`, each host name is covered separately.

An alternative without `EnvoyFilter`: a `VirtualService` route can add the same header with `headers.response.add`, but only for its own routes. `EnvoyFilter` patches Envoy's internal configuration, so check it after Istio upgrades.
