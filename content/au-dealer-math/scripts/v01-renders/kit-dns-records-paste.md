# Kit DNS records for audealermath.com.au

**Add these at VentraIP DNS panel for `audealermath.com.au`.**

Three A records, all on apex (`@` / root domain — leave Name blank if that's how VentraIP shows it):

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `@` | `3.13.222.255` | 3600 |
| A | `@` | `3.13.246.91` | 3600 |
| A | `@` | `3.130.60.26` | 3600 |

**These are Kit's load-balanced server IPs** — three records on the same name = round-robin DNS for redundancy.

## After adding records

1. Save changes at VentraIP
2. Wait 5-30 min (usually faster for fresh domains)
3. Come back to Kit's modal, click **Validate**
4. Kit verifies and the custom domain becomes available

## Once Kit verifies

- AUDM cheatsheet page Settings → Domain name tab
- Custom Domain combobox: select `audealermath.com.au`
- Page URL slug: `cheatsheet`
- Final URL: `audealermath.com.au/cheatsheet`
- Update YT metadata file with new URL

## Troubleshooting

- **DNS not propagating after 30 min:** check VentraIP records were saved correctly. Try `nslookup audealermath.com.au` to verify the IPs return one of `3.13.222.255` / `3.13.246.91` / `3.130.60.26`
- **"Verification Failed" in Kit:** click Validate again after 10 min. DNS sometimes propagates unevenly across Kit's verification servers
- **VentraIP only allows one A record per name:** unusual but possible. Contact VentraIP support — they allow multiple in standard DNS panel

## Reference

- Kit help: https://help.kit.com/en/articles/3107877-how-to-use-a-custom-domain-for-landing-pages
- VentraIP support: vip.ventraip.com.au support tickets
