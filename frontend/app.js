const state = { invoices: [], transactions: [] };
const $ = (selector) => document.querySelector(selector);
const money = (value) => new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN', maximumFractionDigits: 0 }).format(value || 0);
const shortId = (id) => `INV-${(id || '').slice(0, 6).toUpperCase()}`;
const dateText = (date) => date ? new Intl.DateTimeFormat('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).format(new Date(date)) : '—';
const initials = (name) => (name || '?').split(' ').slice(0, 2).map((part) => part[0]).join('').toUpperCase();

async function api(path, options) {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!response.ok) { const detail = await response.json().catch(() => ({})); throw new Error(detail.detail || `Request failed (${response.status})`); }
  return response.status === 204 ? null : response.json();
}

function render() {
  const paid = state.invoices.filter((invoice) => invoice.status === 'paid');
  const outstanding = state.invoices.filter((invoice) => invoice.status !== 'paid');
  $('#total-collected').textContent = money(paid.reduce((sum, invoice) => sum + invoice.amount_ngn, 0));
  $('#total-outstanding').textContent = money(outstanding.reduce((sum, invoice) => sum + invoice.amount_ngn, 0));
  $('#paid-count').textContent = paid.length;
  $('#nav-invoice-count').textContent = state.invoices.length;
  $('#invoice-rows').innerHTML = state.invoices.length ? state.invoices.map((invoice) => `<tr><td><span class="invoice-id">${shortId(invoice.id)}</span></td><td><div class="customer-cell"><span class="customer-badge">${initials(invoice.customer_name)}</span>${escapeHtml(invoice.customer_name)}</div></td><td><span class="date-cell">${dateText(invoice.due_date)}</span></td><td><span class="amount-cell">${money(invoice.amount_ngn)}</span></td><td><span class="status ${invoice.status}">${invoice.status}</span></td><td class="row-actions" data-pay="${invoice.id}" title="${invoice.status === 'paid' ? 'Paid' : 'Mark as paid'}">•••</td></tr>`).join('') : '<tr><td colspan="6" class="empty-table">No invoices yet. Create your first invoice to get started.</td></tr>';
  $('#activity-list').innerHTML = state.transactions.length ? state.transactions.slice().reverse().slice(0, 4).map((tx) => `<div class="activity-item"><span class="activity-icon paid">✓</span><div class="activity-copy"><strong>Payment received</strong><span>${shortId(tx.invoice_id)} · ${dateText(tx.paid_at)}</span></div><span class="activity-amount">+${money(tx.amount_ngn)}</span></div>`).join('') : '<div class="empty-state">No payment activity yet.</div>';
}

function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char])); }
async function loadData() { try { [state.invoices, state.transactions] = await Promise.all([api('/invoices'), api('/transactions')]); render(); } catch (error) { showToast(error.message); } }
async function checkHealth() { try { const health = await api('/health'); $('#health-dot').classList.add('online'); $('#health-label').textContent = `${health.env} · API online`; $('#footer-version').textContent = health.version; } catch { $('#health-label').textContent = 'API unavailable'; } }
function showToast(message) { const toast = $('#toast'); toast.textContent = message; toast.classList.add('show'); setTimeout(() => toast.classList.remove('show'), 3200); }
function toggleModal(open) { $('#invoice-modal').hidden = !open; if (open) { $('#invoice-form').reset(); $('#form-error').textContent = ''; $('#invoice-form input[name="customer_name"]').focus(); } }

$('#open-invoice').addEventListener('click', () => toggleModal(true)); $('#open-invoice-2').addEventListener('click', () => toggleModal(true)); $('#close-modal').addEventListener('click', () => toggleModal(false));
$('#invoice-modal').addEventListener('click', (event) => { if (event.target === $('#invoice-modal')) toggleModal(false); });
$('#invoice-form').addEventListener('submit', async (event) => { event.preventDefault(); const form = new FormData(event.target); const error = $('#form-error'); error.textContent = ''; try { await api('/invoices', { method: 'POST', body: JSON.stringify({ customer_name: form.get('customer_name'), amount_ngn: Number(form.get('amount_ngn')), due_date: form.get('due_date') }) }); toggleModal(false); await loadData(); showToast('Invoice created successfully'); } catch (requestError) { error.textContent = requestError.message; } });
$('#invoice-rows').addEventListener('click', async (event) => { const action = event.target.closest('[data-pay]'); if (!action) return; const invoice = state.invoices.find((item) => item.id === action.dataset.pay); if (!invoice || invoice.status === 'paid') return showToast('This invoice is already paid'); if (!confirm(`Mark ${shortId(invoice.id)} as paid?`)) return; try { await api(`/invoices/${invoice.id}/pay`, { method: 'POST' }); await loadData(); showToast('Payment recorded'); } catch (error) { showToast(error.message); } });
$('#invoice-search').addEventListener('input', (event) => { const query = event.target.value.toLowerCase(); document.querySelectorAll('#invoice-rows tr').forEach((row) => { row.hidden = query && !row.textContent.toLowerCase().includes(query); }); });
checkHealth(); loadData();
